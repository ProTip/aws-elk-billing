import os, sys, urllib3
urllib3.disable_warnings()
sys.path.append(os.path.join(os.path.dirname(__file__)))
#pwd = os.path.dirname(__file__)
'''
added head source directory in path for import from any location and relative testing and pwd for open() relative files
'''
from tools.tools import Tools
import boto3


if __name__ == '__main__':
  
    # you must provide your credentials in the recomanded way, here we are
    # passing it by ENV variables
    s3 = boto3.client('s3')

    #initialize the tools class
    tools = Tools(s3)

    # checking for established connections between E-L-K
    tools.check_elk_connection()

    # function to index the default template mapping of the data
    tools.index_template()

    # getting the required buckets names to index from get_s3_bucket_dir_to_index()
    s3_dir_to_index = tools.get_s3_bucket_dir_to_index()
    if s3_dir_to_index == 1:
        print 'I could not find any billing report under Bucket ', os.environ['S3_BUCKET_NAME'], ' under Path ', os.environ['S3_REPORT_PATH']
        sys.exit(1)

    # downloading the csv file with get_req_csv_from_s3() and then calling the index_csv() to index it in our elasticsearch
    for dir_name in s3_dir_to_index:
        gzip_filename = tools.get_latest_zip_filename(dir_name)
        csv_filename = tools.get_req_csv_from_s3(dir_name, gzip_filename)
        print(gzip_filename,csv_filename)
        tools.index_csv(csv_filename, dir_name)

    # function to index deafualt dashboards, viasualization and search mapping in the .kibana index of elasticsearch
    # kibana is indexed at last because the data will be ready to index at this time
    tools.index_kibana()

    # delete the intermediate files
    tools.delete_csv_json_files()

    # /sbin/init is not working so used this loop to keep the docker up, Have to change it!
    while(True):
        pass

