#!/bin/bash

#Import visualisation json file if that doesn't exist for AWS
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

#Import visualisation json file if that doesn't exist for gCloud
CONTENT=`curl -XGET "http://elasticsearch:9200/.kibana/visualization/gCloud_cost-per-infrastucture-component-usage"`;
if [[ $CONTENT == *'"found":false'* ]]
then
    curl -XPUT "http://elasticsearch:9200/.kibana/visualization/gCloud_cost-per-infrastucture-component-usage" -d "`cat gCloud_cost_per_infrastucture_component_usage.json`";
fi

CONTENT=`curl -XGET "http://elasticsearch:9200/.kibana/visualization/gCloud-Pi-chart-cost-per-service"`;
if [[ $CONTENT == *'"found":false'* ]]
then
    curl -XPUT "http://elasticsearch:9200/.kibana/visualization/gCloud-Pi-chart-cost-per-service" -d "`cat gCloud_Pi_chart_cost_per_service.json`";
fi

CONTENT=`curl -XGET "http://elasticsearch:9200/.kibana/visualization/gCloud-Pi-chart-cost-per-service-group"`;
if [[ $CONTENT == *'"found":false'* ]]
then
    curl -XPUT "http://elasticsearch:9200/.kibana/visualization/gCloud-Pi-chart-cost-per-service-group" -d "`cat gCloud_Pi_chart_cost_per_service_group.json`";
fi

CONTENT=`curl -XGET "http://elasticsearch:9200/.kibana/visualization/gCloud-Pi-chart-for-project"`;
if [[ $CONTENT == *'"found":false'* ]]
then
    curl -XPUT "http://elasticsearch:9200/.kibana/visualization/gCloud-Pi-chart-for-project" -d "`cat gCloud_Pi_chart_for_project.json`";
fi


CONTENT=`curl -XGET "http://elasticsearch:9200/.kibana/visualization/gCloud-Pi-chart-requests-total-cost"`;
if [[ $CONTENT == *'"found":false'* ]]
then
    curl -XPUT "http://elasticsearch:9200/.kibana/visualization/gCloud-Pi-chart-requests-total-cost" -d "`cat gCloud_Pi_chart_requests_total_cost.json`";
fi

CONTENT=`curl -XGET "http://elasticsearch:9200/.kibana/visualization/gCloud-Pi-chat-cost-per-infrastructure-components"`;
if [[ $CONTENT == *'"found":false'* ]]
then
    curl -XPUT "http://elasticsearch:9200/.kibana/visualization/gCloud-Pi-chat-cost-per-infrastructure-components" -d "`cat gCloud_Pi_chat_cost_per_infrastructure_components.json`";
fi

CONTENT=`curl -XGET "http://elasticsearch:9200/.kibana/visualization/gCloud-Top-5-used-service-split-daily"`;
if [[ $CONTENT == *'"found":false'* ]]
then
    curl -XPUT "http://elasticsearch:9200/.kibana/visualization/gCloud-Top-5-used-service-split-daily" -d "`cat gCloud_Top_5_used_service_split_daily.json`";
fi

CONTENT=`curl -XGET "http://elasticsearch:9200/.kibana/visualization/gCloud-top-20-cost-by-project-service"`;
if [[ $CONTENT == *'"found":false'* ]]
then
    curl -XPUT "http://elasticsearch:9200/.kibana/visualization/gCloud-top-20-cost-by-project-service" -d "`cat gCloud_top_20_cost_by_project_service.json`";
fi

CONTENT=`curl -XGET "http://elasticsearch:9200/.kibana/visualization/gCloud-total-cost-Pi-chart-for-separate-service"`;
if [[ $CONTENT == *'"found":false'* ]]
then
    curl -XPUT "http://elasticsearch:9200/.kibana/visualization/gCloud-total-cost-Pi-chart-for-separate-service" -d "`cat gCloud_total_cost_Pi_chart_for_separate_service.json`";
fi

CONTENT=`curl -XGET "http://elasticsearch:9200/.kibana/visualization/gCloud_Cost"`;
if [[ $CONTENT == *'"found":false'* ]]
then
    curl -XPUT "http://elasticsearch:9200/.kibana/visualization/gCloud_Cost" -d "`cat gCloud_Cost.json`";
fi