import pyelasticsearch as pyes
import boto3
import time
import socket
import sys
from datetime import datetime as dtdt
from datetime import date as dtd
from dateutil.relativedelta import relativedelta
import subprocess
import os


def check_connection():
    elasticsearch_socket = socket.socket()
    logstash_socket = socket.socket()
    kibana_socket = socket.socket()

    for _ in range(15):
        try:
            print 'Checking if Elasticsearch container has started to listen to 9200'
            elasticsearch_socket.connect(('elasticsearch', 9200))
            print 'Great Elasticsearch is listening on 9200, 9300 :)'
            break
        except Exception as e:
            print(
                "Something's wrong with Elasticsearch. Exception is %s" %
                (e))
            print 'I will retry after 4 seconds'
            time.sleep(4)

    for _ in range(15):
        try:
            print 'Checking if Logstash container has started to listen to 5140'
            logstash_socket.connect(('logstash', 5140))
            print 'Great Logstash is listening on 5140 :)'
            break
        except Exception as e:
            print("Something's wrong with Logstash. Exception is %s" % (e))
            print 'I will retry after 4 seconds'
            time.sleep(4)

    for _ in range(15):
        try:
            print 'Checking if Kibana container has started to listen to 5160'
            kibana_socket.connect(('kibana', 5601))
            print 'Great Kibana is listening on 5601 :)'
            break
        except Exception as e:
            print("Something's wrong with Kibana. Exception is %s" % (e))
            print 'I will retry after 4 seconds'
            time.sleep(4)

    elasticsearch_socket.close()
    logstash_socket.close()
    kibana_socket.close()


def get_req_csv_from_s3(monthly_dir_name):
    # timestamp
    timestamp = time.strftime('%H_%M')

    # monthly_dir_name for aws s3 directory format for getting the correct json file
    # json file name
    latest_json_file_name = path_name_s3_billing + '/' + monthly_dir_name\
        + path_name_s3_billing + '-Manifest.json'

    # download the jsonfile as getfile_$time.json from s3
    s3.download_file(
        bucketname,
        latest_json_file_name,
        'getfile' +
        timestamp +
        '.json')

    # read the json file to get the latest updated version of csv
    f = open('getfile' + timestamp + '.json', 'r')
    content = eval(f.read())
    latest_gzip_filename = content['reportKeys'][0]
    f.close()

    # the local filename formated for compatibility with the go lang code
    local_gz_filename = 'billing_report_' + timestamp + '_' + \
        dtdt.strptime(monthly_dir_name.split('-')[0], '%Y%m%d').strftime('%Y-%m') + '.csv.gz'
    local_csv_filename = local_gz_filename[:-3]

    # downloading the zipfile from s3
    s3.download_file(bucketname, latest_gzip_filename, local_gz_filename)

    # upzip and replace the .gz file with .csv file
    print("Extracting latest csv file")
    process_gunzip = subprocess.Popen(
        ['gunzip -v ' + local_gz_filename], shell=True)
    return local_csv_filename


def index_csv(filename, dir_name, template=True):
    if template:
        # Index aws mapping json file
        status = subprocess.Popen(
            ['curl -XPUT elasticsearch:9200/_template/aws_billing -d "`cat /aws-elk-billing/aws-billing-es-template.json`"'],
            shell=True)
        if status.wait() != 0:
            print 'Something went wrong while creating mapping index'
            sys.exit(1)
        else:
            print 'ES mapping created :)'
    else:
        print 'Template Already Exist'

    # DELETE earlier aws-billing* index if exists for the current indexing month
    # current month index format (name)
    index_format = dtdt.strptime(
        dir_name.split('-')[0],
        '%Y%m%d').strftime('%Y.%m')
    os.environ['file_y_m'] = index_format
    # have to change the name of the index in logstash index=>indexname

    status = subprocess.Popen(
        ['curl -XGET elasticsearch:9200/_cat/indices/?v'],
        shell=True)

    status = subprocess.Popen(
        ['curl -XDELETE elasticsearch:9200/aws-billing-' + index_format], shell=True)
    if status.wait() != 0:
        print 'I think there are no aws-billing* indice or it is outdated, its OK main golang code will create a new one for you :)'
    else:
        print 'aws-billing* indice deleted or Not found, its OK main golang code will create a new one for you :)'

    # Run the main golang code to parse the billing file and send it to
    # Elasticsearch over Logstash
    status = subprocess.Popen(
        ['go run /aws-elk-billing/main.go --file /aws-elk-billing/' + filename], shell=True)
    if status.wait() != 0:
        print 'Something went wrong while getting the file reference or while talking with logstash'
        sys.exit(1)
    else:
        print 'AWS Billing report sucessfully parsed and indexed in Elasticsearch via Logstash :)'


def index_kibana():
    # Index Kibana dashboard
    status = subprocess.Popen(
        ['(cd /aws-elk-billing/kibana; bash orchestrate_dashboard.sh)'],
        shell=True)
    if status.wait() != 0:
        print 'Kibana dashboard failed to indexed to .kibana index in Elasticsearch'
        sys.exit(1)
    else:
        print 'Kibana dashboard sucessfully indexed to .kibana index in Elasticsearch :)'

    # Index Kibana visualization
    status = subprocess.Popen(
        ['(cd /aws-elk-billing/kibana; bash orchestrate_visualisation.sh)'],
        shell=True)
    if status.wait() != 0:
        print 'Kibana visualization failed to indexed to .kibana index in Elasticsearch'
        sys.exit(1)
    else:
        print 'Kibana visualization sucessfully indexed to .kibana index in Elasticsearch :)'

# checking for established connection
check_connection()

# you must provide your credentials in the recomanded way, here we are
# passing it by ENV variables
s3 = boto3.client('s3')

# give the correct bucket name for your s3 billing bucket
bucketname = os.environ['S3_BUCKET_NAME']
path_name_s3_billing = os.environ['S3_BILL_PATH_NAME']
key_names = s3.list_objects(
    Bucket='priceboard-billing',
    Prefix='/billing_report_for_elk_dashboard/',
    Delimiter='/')
s3_dir_names = []

for keys in key_names['CommonPrefixes']:
    s3_dir_names.append(keys['Prefix'].split('/')[-2])

s3_dir_names.sort()
es = pyes.ElasticSearch('http://elasticsearch:9200')
index_list = es.get_mapping('aws-billing*').keys()
index_time = []
for i in index_list:
    if i:
        index_time.append(es.search(index=i, size=1, query={"query": {"match_all": {}}})[
                          'hits']['hits'][0]['_source']['@timestamp'])

index_time.sort(reverse=True)

dir_start = 0
dir_end = None
template = True

if index_time:
    current_dir = dtd.today().strftime('%Y%m01') + '-' + (dtd.today() + \
                            relativedelta(months=1)).strftime('%Y%m01')

    last_ind_dir = index_time[0].split('T')[0].replace('-', '')
    last_ind_dir = dtdt.strptime(last_ind_dir, '%Y%m%d').strftime('%Y%m01') + '-' + (
        dtdt.strptime(last_ind_dir, '%Y%m%d') + relativedelta(months=1)).strftime('%Y%m01')
    dir_start = s3_dir_names.index(last_ind_dir)
    dir_end = s3_dir_names.index(current_dir) + 1
    template = False

index_kibana()
print('Months to be indexed: %s', s3_dir_names[dir_start:dir_end])

for dir_name in s3_dir_names[dir_start:dir_end]:
    csv_filename = get_req_csv_from_s3(dir_name)
    index_csv(csv_filename, dir_name, template)
    template = False

# delete all getfile, csv files and part downloading files after indexing over
process_delete_csv = subprocess.Popen(
    ["find /aws-elk-billing -name 'billing_report_*' -exec rm -f {} \;"],
    shell=True)
process_delete_json = subprocess.Popen(
    ["find /aws-elk-billing -name 'getfile*' -exec rm -f {} \;"], shell=True)

# /sbin/init is not working so used this loop to keep the docker up, Have to change it!
while(True):
    pass
