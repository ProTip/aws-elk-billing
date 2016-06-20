import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__)))
#pwd = os.path.dirname(__file__)
'''
added head source directory in path for import from any location and relative testing and pwd for open() relative files
'''
from tools.tools import Tools
import boto3


if __name__ == '__main__':

    #initialize the tools class with the overloaded constructor
    tools = Tools()

    # checking for established connections between E-L-K
    tools.check_elk_connection()

    # function to index the default template mapping of the data
    tools.index_template()
    
    # index a sample test file with sum of unblended cost 1.24185686
    tools.index_csv('/test/sample/test_ub_cost_2000-01.csv', '20000101-20000102')

    # function to index deafualt dashboards, viasualization and search mapping in the .kibana index of elasticsearch
    # kibana is indexed at last because the data will be ready to index at this time
    tools.index_kibana()

    # /sbin/init is not working so used this loop to keep the docker up, Have to change it!
    #while(True):
    #    pass

