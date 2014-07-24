package main

import (
	_ "fmt"
	"testing"
)

func TestCostAllocationMatcher(t *testing.T) {
	if !monthlyCostAllocationMatcher.MatchString("376681487066-aws-cost-allocation-2013-06.csv") {
		t.Fail()
	}
}

func TestDetailedBillingWithResourcesMatcher(t *testing.T) {
	if !detailedBillingWithResourcesMatcher.MatchString("376681487066-aws-billing-detailed-line-items-with-resources-and-tags-2014-03.csv") {
		t.Fail()
	}
}

func TestBillingReportTypeString(t *testing.T) {
	report := &BillingReport{}
	report.ReportType = MonthlyCostAllocation
	if report.TypeString() != "aws_billing_monthly" {
		t.Fail()
	}
	report.ReportType = DetailedBillingWithResourcesAndTags
	if report.TypeString() != "aws_billing_hourly" {
		t.Fail()
	}
}

func TestParseReport(t *testing.T) {
	in := make(chan []string)
	out := make(chan map[string]interface{})
	report := OpenBillingReport("test-2014-06.csv")
	report.Mapper = FieldMapper{
		"LinkedAccountId": {
			"041869798014": {
				"AccountName": "MYOB Advanced",
			},
		},
	}
	go ParseRecord(in, out, report)
	values, _ := report.csvReader.Read()
	in <- values
	close(in)
}
