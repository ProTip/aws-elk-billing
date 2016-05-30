#!/bin/bash

#Import dashboard json file

curl -XPUT "http://elasticsearch:9200/.kibana/dashboard/AWS-Billing-DashBoard" -d "`cat kibana_dashboard.json`"
