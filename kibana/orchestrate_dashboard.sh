#!/bin/bash

#Import the default AWS-Billing-DashBoard json file if there is no such dashboard present

CONTENT=`curl -XGET "http://elasticsearch:9200/.kibana/dashboard/AWS-Billing-DashBoard"`;

if [[ $CONTENT == *'"found":true'* ]]
then
    echo "Dashboard With Default Name Is Already There!";
else
    echo "Default Dashboard Is Being Created!";
    curl -XPUT "http://elasticsearch:9200/.kibana/dashboard/AWS-Billing-DashBoard" -d "`cat kibana_dashboard.json`";
fi
