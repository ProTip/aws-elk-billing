#!/bin/bash

#Import visualisation json file if that doesn't exist
CONTENT=`curl -XGET "http://elasticsearch:9200/.kibana/visualization/finalVisualization_5days_30min_row_split"`;
if [[ $CONTENT == *'"found":false'* ]]
then
    curl -XPUT "http://elasticsearch:9200/.kibana/visualization/finalVisualization_5days_30min_row_split" -d "`cat finalVisualization_5days_30min_row_split.json`";
fi


CONTENT=`curl -XGET "http://elasticsearch:9200/.kibana/visualization/finalVisualization_5days_30min_line_split"`;
if [[ $CONTENT == *'"found":false'* ]]
then
    curl -XPUT "http://elasticsearch:9200/.kibana/visualization/finalVisualization_5days_30min_line_split" -d "`cat finalVisualization_5days_30min_line_split.json`";
fi


CONTENT=`curl -XGET "http://elasticsearch:9200/.kibana/visualization/api_call_table"`;
if [[ $CONTENT == *'"found":false'* ]]
then
    curl -XPUT "http://elasticsearch:9200/.kibana/visualization/api_call_table" -d "`cat api_call_table.json`";
fi


CONTENT=`curl -XGET "http://elasticsearch:9200/.kibana/visualization/Total_UnblendedCost"`;
if [[ $CONTENT == *'"found":false'* ]]
then
    curl -XPUT "http://elasticsearch:9200/.kibana/visualization/Total_UnblendedCost" -d "`cat Total_UnblendedCost.json`";
fi


CONTENT=`curl -XGET "http://elasticsearch:9200/.kibana/visualization/Spot_vs_OnDemand_EC2"`;
if [[ $CONTENT == *'"found":false'* ]]
then
    curl -XPUT "http://elasticsearch:9200/.kibana/visualization/Spot_vs_OnDemand_EC2" -d "`cat Spot_vs_OnDemand_EC2.json`";
fi


CONTENT=`curl -XGET "http://elasticsearch:9200/.kibana/visualization/Split_bars_daily"`;
if [[ $CONTENT == *'"found":false'* ]]
then
    curl -XPUT "http://elasticsearch:9200/.kibana/visualization/Split_bars_daily" -d "`cat Split_bars_daily.json`";
fi


CONTENT=`curl -XGET "http://elasticsearch:9200/.kibana/visualization/S3_Api_Calls_daily"`;
if [[ $CONTENT == *'"found":false'* ]]
then
    curl -XPUT "http://elasticsearch:9200/.kibana/visualization/S3_Api_Calls_daily" -d "`cat S3_Api_Calls_daily.json`";
fi


CONTENT=`curl -XGET "http://elasticsearch:9200/.kibana/visualization/Pi-chart-for-seperate-services"`;
if [[ $CONTENT == *'"found":false'* ]]
then
    curl -XPUT "http://elasticsearch:9200/.kibana/visualization/Pi-chart-for-seperate-services" -d "`cat Pi-chart-for-seperate-services.json`";
fi


CONTENT=`curl -XGET "http://elasticsearch:9200/.kibana/visualization/Cost_For_AmazonS3_requests"`;
if [[ $CONTENT == *'"found":false'* ]]
then
    curl -XPUT "http://elasticsearch:9200/.kibana/visualization/Cost_For_AmazonS3_requests" -d "`cat Cost_For_AmazonS3_requests.json`";
fi


CONTENT=`curl -XGET "http://elasticsearch:9200/.kibana/visualization/Top-5-used-service-split-daily"`;
if [[ $CONTENT == *'"found":false'* ]]
then
    curl -XPUT "http://elasticsearch:9200/.kibana/visualization/Top-5-used-service-split-daily" -d "`cat top_5_used_service_split_daily.json`";
fi
