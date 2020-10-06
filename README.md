# aws-elk-billing [![Build Status](https://travis-ci.org/PriceBoardIn/aws-elk-billing.svg?branch=master)](https://travis-ci.org/PriceBoardIn/aws-elk-billing)
![Alt text](https://raw.githubusercontent.com/alecs/aws-elk-billing/master/screenshots/dashboard_black.png "Overview")

**This is a fork of [Greg's repo](https://github.com/ProTip/aws-elk-billing) (https://github.com/ProTip/aws-elk-billing)**

Versions of the 4 containers were slightly changed because some of them were not found.

## To do

* add GCloud billing support and dashboard
* update stack to OpenDistro with OAuth

## Overview
 
aws-elk-billing is a combination of configuration snippets and tools to assist with indexing AWS programatic billing access files(CSV's) and visualizing the data using Kibana.

Currently it supports `AWS Cost and Usage Report` type, although it might work for other [AWS Billing Report Types](http://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/detailed-billing-reports.html#other-reports) which contains some extra columns along with all the columns from `AWS Cost and Usage Report`.

You can create `AWS Cost and Usage Report` at https://console.aws.amazon.com/billing/home#/reports

or follow instructions at http://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/detailed-billing-reports.html#turnonreports


### Architecture
There are Four Docker containers. 

1. [Elasticsearch 2.3.3](https://hub.docker.com/r/priceboard/elasticsearch) (https://github.com/PriceBoardIn/elasticsearch/tree/2.3.3)
2. [Kibana](https://hub.docker.com/r/priceboard/kibana) (https://github.com/PriceBoardIn/kibana)
3. [Logstash](https://hub.docker.com/r/priceboard/logstash) (https://github.com/PriceBoardIn/logstash)
4. aws-elk-billing (Refer: Dockerfile of this repository)

Integration among the 4 containers is done with `docker-compose.yml`


### Primary Components
Task | Files
------------ | -------------
Logstash configuration | `logstash.conf`
Kibana configuration | `kibana.yml`
Elasticsearch index mapping | `aws-billing-es-template.json`
Indexing Kibana dashboard| `kibana/orchestrate_dashboard.sh`
Indexing Kibana visualisation| `kibana/orchestrate_visualisation.sh`
Indexing Kibana default index (This file is just for reference purpose, we will automate this part eventually)| `kibana/orchestrate_kibana.sh`
Parsing the aws-billing CSV's and sending to logstash | `main.go`
Connecting the dots: `Wait` for ELK Stack to start listening on their respective ports, `downloads`, `extracts` the latest compressed billing report from S3, `XDELETE` previous index of the current month, `Index mapping`, `Index kibana_dashboard`, `Index kibana_visualization` and finally executes `main.go` | `orchestrate.py`
Integrating all 4 containers | `Dockerfile`, `docker-compose.yml`

## Getting Started
Clone the Repository and make sure that no process is listening to the ports used by all these dockers.

Ports | Process
------------ | -------------
9200, 9300 | Elasticsearch
5160 | Kibana
5140 | Logstash

### Set S3 credentials and AWS Billing bucket and directory name
Rename [prod.sample.env](https://github.com/PriceBoardIn/aws-elk-billing/blob/master/prod.sample.env) to `prod.env` and provide values for the following keys `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `S3_BUCKET_NAME`, `S3_REPORT_PATH`

##### `S3_BUCKET_NAME` = S3 bucket name (Refer the image below)
##### `S3_REPORT_PATH` = Report path (Refer the image below)
##### `S3_REPORT_NAME` = Report name (Refer the image below)

`prod.env` is added in `.gitignore` so that you don't push your credentials upstream accidentally.

![Alt text](https://raw.githubusercontent.com/PriceBoardIn/aws-elk-billing/master/screenshots/aws cost and usage reports console.png)

### Run Docker
The entire process is automated through scripts and docker. All the components would be downloaded automatically inside your docker

1. ```sudo docker-compose up -d```
2. View `Kibana` at http://localhost:5601

    2.1 Use the **index pattern** as `aws-billing-*` and select the **time field** as `lineItem/UsageStartDate`
    
    2.2 `Kibana AWS Billing Dashboard` http://localhost:5601/app/kibana#/dashboard/AWS-Billing-DashBoard
    
    2.3 For MAC replace localhost with the ip of docker-machine
    To find IP of docker-machine `docker-machine ip default`

3   . `sudo docker-compose down` to shutdown all the docker containers.

## Gotchas

* `aws-elk-billing` container will take time while running the following two process `[Filename: orchestrate.py]`.
    1. Downloading and extracting AWS Billing report from AWS S3.
    2. Depending on the size of AWS Billing CSV report `main.go` will take time to index all the data to Elasticsearch via Logstash.
* You can view the dashboard in kibana, even while `main.go` is still indexing the data.
* In order to index new data, you'll have to run `docker-compose up -d` again.
