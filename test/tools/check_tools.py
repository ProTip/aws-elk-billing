import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__),'..','..','..'))
'''
added head source directory in path for import from any location
'''
from unittest import TestCase
from nose.tools import assert_equals
from nose.tools import assert_items_equal
import logging
from tools.tools import Tools
import boto3
import subprocess
import simplejson

log = logging.getLogger(__name__)
TestCase.maxDiff = None
TestCase.longMessage = True


class Test_Functions:

    def __init__(self):
        self.check_tools = Tools()

    def test_check_elk_connection(self):
        assert_equals(
            self.check_tools.check_elk_connection(),
            True,
            'Must return True for E-L-K connections successfull'
        )

    def test_ub_cost(self):
        result = subprocess.check_output(['curl -XGET "http://elasticsearch:9200/aws-billing-2016.06/_search" -d "`cat /aws-elk-billing/test/tools/aggregate.json`"'],
            shell=True, stderr=subprocess.PIPE)
        print(result)
        result = simplejson.loads(result)
        sum_ub_cost = result["aggregations"]["sum_ub_cost"]["value"]
        subprocess.check_output(['echo -e "POST /containers/elasticsearch_1/kill?signal=HUP HTTP/1.0\r\n" | nc -U /var/run/docker.sock'], shell=True, stderr=subprocess.PIPE)
        subprocess.check_output(['echo -e "POST /containers/kibana_1/kill?signal=HUP HTTP/1.0\r\n" | nc -U /var/run/docker.sock'], shell=True, stderr=subprocess.PIPE)
        subprocess.check_output(['echo -e "POST /containers/logstash_1/kill?signal=HUP HTTP/1.0\r\n" | nc -U /var/run/docker.sock'], shell=True, stderr=subprocess.PIPE)
        assert_equals(
            float(format(sum_ub_cost,'.3f')),
            1.242,
            'Must return the exact sum as the csv file'
        )
