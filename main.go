// aws-billing project main.go
package main
import (
	"encoding/csv"
	"encoding/json"
	"flag"
	"fmt"
	"io"
	"math"
	"net"
	"os"
	"regexp"
	"runtime"
	"strconv"
	"strings"
	"sync"
	"time"
)

var (
	tagMatcher                          = regexp.MustCompile("(user|aws):.*")
	dateMonthMatcher                    = regexp.MustCompile(`\d{4}-\d{2}`)
	monthlyCostAllocationMatcher        = regexp.MustCompile(`.*aws-cost-allocation.*`)
	detailedBillingWithResourcesMatcher = regexp.MustCompile(`.*billing-report.*`)
	ReportMatchers                      = []*regexp.Regexp{monthlyCostAllocationMatcher, detailedBillingWithResourcesMatcher}
	wg                                  = sync.WaitGroup{}

	// Flag variables
	file            = flag.String("file", "billing_report_2016-05.csv", "CSV billing file to load.")
	logstashAddress = flag.String("logstash-address", "db.logstash.priceboard.in:5140", "Address and port for the logstash tcp listener.")
	concurrency     = flag.Int("concurrency", 2, "Number of cores to use.")
	//accountsFile    = flag.String("accounts-file", "aws-cost-allocation-2014-06.csv", "CSV file containing LinkedAccountId and account LinkedAccountName")
)

var FieldTypes = map[string]func(s string, report *BillingReport) interface{} {
	"PayerAccountId":         ParseInt,
	"RateId":                 ParseInt,
	"SubscriptionId":         ParseInt,
	"PricingPlanId":          ParseInt,
	"UsageQuantity":          ParseFloat,
	"BlendedRate":            ParseFloat,
	"BlendedCost":            ParseFloat,
	"UnBlendedRate":          ParseFloat,
	"UnBlendedCost":          ParseFloat,
	"TotalCost":              ParseFloat,
	"Cost":                   ParseFloat,
	"CostBeforeTax":          ParseFloat,
	"Credits":                ParseFloat,
	"UsageStartDate":         ParseDate,
	"UsageEndDate":           ParseDate,
	"BillingPeriodStartDate": ParseBillingPeriodDate,
	"BillingPeriodEndDate":   ParseBillingPeriodDate,
}

type DetailedLineItem struct {
	InvoiceID       string
	PayerAccountId  int
	LinkedAccountId int
}

const (
	DetailedBillingWithResourcesAndTags = iota
	MonthlyCostAllocation               = iota
)

type FieldMapper map[string]map[interface{}]map[string]interface{}

type BillingReport struct {
	CsvFileName   string
	InvoicePeriod time.Time
	ReportType    int
	Fields        []string
	csvReader     *csv.Reader
	Mapper        FieldMapper
}

func main() {
	flag.Parse()
	fmt.Println("AWS billing CSV report parser!")
	var out = make(chan []byte)
	fmt.Println("out after make(chan []byte) is %v", out)
	go PublishRecord(out)
	//var csvFileName = "376681487066-aws-billing-detailed-line-items-with-resources-and-tags-2014-06.csv"

	report := OpenBillingReport(*file)

	/*if *accountsFile != "" {
		accountReport := OpenBillingReport(*accountsFile)
		report.Mapper = ReportToAccountFieldMap(accountReport)
	}*/

	valuesSink := make(chan []string)
	reportSinks := make([]chan map[string]interface{}, 0, 0)
	jsonSinks := make([]chan []byte, 0, 0)

	for i := 0; i < runtime.GOMAXPROCS(*concurrency); i++ {
		reportSink := make(chan map[string]interface{})
		jsonSink := make(chan []byte)
		reportSinks = append(reportSinks, reportSink)
		jsonSinks = append(jsonSinks, jsonSink)
		go ParseRecord(valuesSink, reportSink, report)
		go RecordToJson(reportSink, jsonSink)
		go PublishRecord(jsonSink)
		wg.Add(3)
	}

	var recordNum int
	for {
		values, err := report.csvReader.Read()
		if err == io.EOF {
			break
		}
		valuesSink <- values
		recordNum += 1
		if math.Mod(float64(recordNum), 10000) == 0 {
			fmt.Println(recordNum)
		}
	}
	close(valuesSink)
	wg.Wait()
}

func ReportToAccountFieldMap(report *BillingReport) FieldMapper {
	mapper := FieldMapper{}
	mapper["LinkedAccountId"] = make(map[interface{}]map[string]interface{})
	for {
		values, err := report.csvReader.Read()
		if err == io.EOF {
			break
		} else if err != nil {
			panic(err.Error())
		}

		var linkedAccountId string
		var linkedAccountName string
		for i, field := range report.Fields {
			if field == "LinkedAccountId" {
				linkedAccountId = values[i]
			}
			if field == "LinkedAccountName" {
				linkedAccountName = values[i]
			}
		}
		if _, ok := mapper["LinkedAccountId"][linkedAccountId]; !ok {
			fmt.Println("Creating map for: ", linkedAccountId)
			mapper["LinkedAccountId"][linkedAccountId] = make(map[string]interface{})
		}
		mapper["LinkedAccountId"][linkedAccountId]["LinkedAccountName"] = linkedAccountName
	}
	return mapper
}

func ParseRecord(in chan []string, out chan map[string]interface{}, report *BillingReport) {
	var parsedValue interface{}
	for values := range in {
		var record = make(map[string]interface{})
		record["Tags"] = make(map[string]interface{})
		record["type"] = report.TypeString()
		for i, field := range report.Fields {
			if f, ok := FieldTypes[field]; ok {
				parsedValue = f(values[i], report)
				record[field] = parsedValue
			} else if tagMatcher.MatchString(field) {
				record["Tags"].(map[string]interface{})[ParseTag(field, report).(string)] = strings.ToLower(values[i])
				parsedValue = strings.ToLower(values[i])
			} else {
				record[field] = values[i]
				parsedValue = values[i]
			}
			if valueMap, ok := report.Mapper[field][parsedValue]; ok {
				for k, v := range valueMap {
					record[k] = v
				}
			}
		}
		out <- record
	}
	close(out)
	wg.Done()
}

func RecordToJson(in chan map[string]interface{}, out chan []byte) {
	for record := range in {
		jbRecord, err := json.Marshal(record)
		if err != nil {
			panic(err.Error())
		}
		out <- jbRecord
	}
	close(out)
	wg.Done()
}

func (report *BillingReport) TypeString() string {
	switch report.ReportType {
	case DetailedBillingWithResourcesAndTags:
		return "aws_billing_hourly"
	case MonthlyCostAllocation:
		return "aws_billing_monthly"
	}
	return ""
}

func OpenBillingReport(csvFileName string) *BillingReport {
	fmt.Println("Opening billing report filename", csvFileName)
	/*
	AWS billing report filename must contain at least yyyy-mm
	*/
	invoicePeriod, err := time.Parse("2006-01", dateMonthMatcher.FindString(csvFileName))
	if err != nil {
		panic(err.Error())
	}
	file, err := os.Open(csvFileName)
	if err != nil {
		panic(err.Error())
	}
	reader := csv.NewReader(file)
	report := &BillingReport{
		CsvFileName:   csvFileName,
		InvoicePeriod: invoicePeriod,
		csvReader:     reader}

	switch {
	case detailedBillingWithResourcesMatcher.MatchString(csvFileName):
		report.ReportType = DetailedBillingWithResourcesAndTags
	case monthlyCostAllocationMatcher.MatchString(csvFileName):
		report.ReportType = MonthlyCostAllocation
	}

	if report.ReportType == MonthlyCostAllocation {
		//Burn one due to comment
		fmt.Println("Monthly cost allocation, skipping comment:")
		fmt.Println(reader.Read())
		reader.FieldsPerRecord = 0
	}
	fields, err := reader.Read()
	if err != nil {
		panic(err.Error())
	}
	report.Fields = fields
	return report
}

func ParseTag(s string, report *BillingReport) interface{} {
	tagParts := strings.Split(s, ":")
	return strings.Join(tagParts, "_")
}

func ParseInt(s string, report *BillingReport) interface{} {
	value, _ := strconv.ParseInt(s, 0, 0)
	return value
}

func ParseUint(s string, report *BillingReport) interface{} {
	value, _ := strconv.ParseUint(s, 0, 0)
	return value
}

func ParseFloat(s string, report *BillingReport) interface{} {
	value, _ := strconv.ParseFloat(s, 0)
	return value
}

func ParseDate(s string, report *BillingReport) interface{} {
	var returnTime time.Time
	var err error
	switch s {
	case "":
		returnTime = report.InvoicePeriod
	default:
		returnTime, err = time.Parse("2006-01-02 15:04:05", s)
		if err != nil {
			panic(err.Error())
		}
	}
	return returnTime.Format(time.RFC3339)
}

func ParseBillingPeriodDate(s string, report *BillingReport) interface{} {
	var returnTime time.Time
	var err error
	switch s {
	case "":
		returnTime = report.InvoicePeriod
	default:
		returnTime, err = time.Parse("2006/01/02 15:04:05", s)
		if err != nil {
			panic(err.Error())
		}
	}
	return returnTime.Format(time.RFC3339)
}

func PublishRecord(in chan []byte) {
	fmt.Println("Publishing record to logstash %v", in)
	con, err := net.DialTimeout("tcp", *logstashAddress, (5 * time.Second))
	if err != nil {
		panic(err.Error())
	}
	for record := range in {
		_, err = con.Write(record)
		if err != nil {
			panic(err.Error())
		}
		_, err = con.Write([]byte("\n"))
		if err != nil {
			panic(err.Error())
		}
	}
	wg.Done()
}
