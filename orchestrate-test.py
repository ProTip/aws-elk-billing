import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__)))
#pwd = os.path.dirname(__file__)
'''
added head source directory in path for import from any location and relative testing and pwd for open() relative files
'''
from tools.tools import Tools
import boto3
import subprocess
import time

if __name__ == '__main__':

    print('Orchestrate-test Running')
    #initialize the tools class
    tools = Tools()

    # checking for established connections between E-L-K
    tools.check_elk_connection()

    # function to index the default template mapping of the data
    tools.index_template()
    
    # index a sample test file with sum of unblended cost 1.24185686
    tools.index_csv('test/sample/test_ub_cost_2016-06.csv', '20160601-20160701')
    # rows of data in the csv, must be given as string
    data_count = '315'
    while(True):
        index_names = subprocess.check_output(['curl -XGET "elasticsearch:9200/_cat/indices/"'], shell=True, stderr=subprocess.PIPE)
        if 'aws-billing-2016.06' in index_names and data_count in index_names:
            break

    index_names = subprocess.check_output(['curl -XGET "elasticsearch:9200/_cat/indices/"'], shell=True, stderr=subprocess.PIPE)
    print(index_names)

    tools.index_kibana()
    tools.delete_csv_json_files()
