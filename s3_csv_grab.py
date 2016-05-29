import boto3
import time
import socket
import sys
import datetime
from dateutil.relativedelta import relativedelta
import subprocess

'''
Todo:
Error Handling
User Interface
'''

# you must provide your credentials in the recomanded way, here we are passing it by ENV variables
s3 = boto3.client('s3')

# give the correct bucket name for your s3 billing bucket
bucketname = 'priceboard-billing'

#timestamp
timestamp = time.strftime('%H_%M')

# generate the aws s3 directory format for getting the correct json file
generate_monthly_dir_name = datetime.date.today().strftime('%Y%m01')+'-'+\
                        (datetime.date.today()+relativedelta(months=1)).strftime('%Y%m01')

# json file name
latest_json_file_name = '/billing_report_for_elk_dashboard/'+generate_monthly_dir_name\
                +'/billing_report_for_elk_dashboard-Manifest.json'

# download the jsonfile as getfile.json from s3
s3.download_file(bucketname,latest_json_file_name,'getfile.json')

# read the json file to get the latest updated version of csv
f = open('getfile.json','r')
content=eval(f.read())
latest_gzip_filename = content['reportKeys'][0]
f.close()

# the local filename formated for compatibility with the go lang code
local_gz_filename = 'billing_report_'+timestamp+'_'+datetime.date.today().strftime('%Y-%m')+'.csv.gz'

# downloading the zipfile from s3
s3.download_file(bucketname,latest_gzip_filename,local_gz_filename)

#upzip and replace the .gz file with .csv file
print("Extracting latest csv file")
process_gunzip = subprocess.Popen(['gunzip -v '+ local_gz_filename],shell=True)
print('Done')


elasticsearch_socket	= socket.socket()
logstash_socket			= socket.socket()
kibana_socket			= socket.socket()

for _ in range(5):
	try:
		print 'Checking if Elasticsearch container has started to listen to 9200'
		elasticsearch_socket.connect(('db.elasticsearch.priceboard.in', 9200))
		break
	except Exception as e:
		print("Something's wrong with Elasticsearch. Exception is %s" % (e))
		print 'I will retry after 4 seconds'
		time.sleep(4)

for _ in range(5):
	try:
		print 'Checking if Logstash container has started to listen to 5140'
		logstash_socket.connect(('db.logstash.priceboard.in', 5140))
		break
	except Exception as e:
		print("Something's wrong with Logstash. Exception is %s" % (e))
		print 'I will retry after 4 seconds'
		time.sleep(4)

for _ in range(5):
	try:
		print 'Checking if Kibana container has started to listen to 5160'
		kibana_socket.connect(('kibana.priceboard.in', 5160))
		break
	except Exception as e:
		print("Something's wrong with Kibana. Exception is %s" % (e))
		print 'I will retry after 4 seconds'
		time.sleep(4)

elasticsearch_socket.close()
logstash_socket.close()
kibana_socket.close()

status = subprocess.Popen(['curl -XDELETE db.elasticsearch.priceboard.in:9200/aws-billing*'], shell=True)
if status.wait() != 0:
	print 'Something went wrong while deleting earlier aws-billing* indice'
	print 'I think there was no aws-billing* indice'
	sys.exit(1)
else:
	print 'aws-billing* indice deleted'

status = subprocess.Popen(['curl -XPUT db.elasticsearch.priceboard.in:9200/_template/aws_billing -d "`cat /aws-elk-billing/aws-billing-es-template.json`"'], shell=True)
if status.wait() != 0:
	print 'Something went wrong while creating mapping index'
	sys.exit(1)
else:
	print 'ES mapping created'

status = subprocess.Popen(['go run /aws-elk-billing/main.go --file /aws-elk-billing/billing_report_'+timestamp+'_2016-05.csv'], shell=True)
if status.wait() != 0:
	print 'Something went wrong while getting the file reference or while talking with logstash'
	sys.exit(1)
else:
	print 'AWS Billing report sucessfully parsed and indexed in Elasticsearch via Logstash :)'

while True:
	pass
