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

log = logging.getLogger(__name__)
TestCase.maxDiff = None
TestCase.longMessage = True


class Test_Functions:

    def __init__(self):
        s3 = boto3.client('s3')
        self.check_tools = Tools(s3)
    
    def test_check_elk_connection(self):
        assert_equals(
            self.check_tools.check_elk_connection(),
            True,
            'Must return True for E-L-K connections successfull'
        )

    def test_get_s3_bucket_dir_to_index(self):
        assert_equals(
            self.check_tools.get_s3_bucket_dir_to_index(),
            ['20160601-20160701'],
            'Must return The non-index months along with the current month'
        )

    def test_get_latest_zip_filename(self):
        assert_items_equal(self.check_tools.get_latest_zip_filename
            ('20160601-20160701'),
            '/billing_report_for_elk_dashboard/20160601-20160701/377f626b-c93d-457c-921a-8e0c85b8244e/billing_report_for_elk_dashboard-1.csv.gz',
            'Must return the local csv file name downloaded'
        )

    def test_get_req_csv_from_s3(self):
        assert_items_equal(self.check_tools.get_req_csv_from_s3
            ('20160601-20160701', '/billing_report_for_elk_dashboard/20160601-20160701/377f626b-c93d-457c-921a-8e0c85b8244e/billing_report_for_elk_dashboard-1.csv.gz'),
            'billing_report_2016-06.csv',
            'Must return the local csv file name downloaded'
        )