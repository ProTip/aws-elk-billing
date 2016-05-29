#!/bin/bash

#Import dashboard json file

curl -XPUT "http://db.elasticsearch.priceboard.in:9200/.kibana/dashboard/AWS-Billing-DashBoard" -d "`cat kibana_dashboard.json`"
