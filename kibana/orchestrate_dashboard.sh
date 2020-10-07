#!/bin/bash

#Import the default AWS-Billing-DashBoard json file if there is no such dashboard present

CONTENT_AWS=`curl -XGET "http://elasticsearch:9200/.kibana/dashboard/AWS-Billing-DashBoard"`;

if [[ $CONTENT_AWS == *'"found":true'* ]]
then
    echo "Dashboard With Default Name Is Already There!";
else
    echo "Default Dashboard Is Being Created!";
    curl -XPUT "http://elasticsearch:9200/.kibana/dashboard/AWS-Billing-DashBoard" -d "`cat kibana_dashboard.json`";
fi

#Import the gCloud-billing-dashBoard json file if there is no such dashboard present

CONTENT_GCLOUD=`curl -XGET "http://elasticsearch:9200/.kibana/dashboard/gCloud-billing-dashboard"`;

if [[ $CONTENT_GCLOUD == *'"found":true'* ]]
then
    echo "Dashboard With Default Name Is Already There!";
else
    echo "Default Dashboard Is Being Created!";
    curl -XPUT "http://elasticsearch:9200/.kibana/dashboard/gCloud-billing-dashboard" -d "`cat gCloud-billing-dashboard.json`";
fi