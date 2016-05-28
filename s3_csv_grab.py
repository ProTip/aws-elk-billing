import boto3
import datetime
from dateutil.relativedelta import relativedelta
import subprocess

'''
Todo:
Error Handling
User Interface
'''

'''
# you must provide your credentials in the recomanded way, here we are passing it by ENV variables
s3 = boto3.client('s3')

# give the correct bucket name for your s3 billing bucket
bucketname = 'priceboard-billing'

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
local_gz_filename = 'billing_report_'+datetime.date.today().strftime('%Y-%m')+'.csv.gz'

# downloading the zipfile from s3
s3.download_file(bucketname,latest_gzip_filename,local_gz_filename)

#upzip and replace the .gz file with .csv file
print("Extracting latest csv file")
process_gunzip = subprocess.Popen(['gunzip -v '+ local_gz_filename],shell=True)
print('Done')
'''

while True:
	pass
