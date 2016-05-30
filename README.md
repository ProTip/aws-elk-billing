# aws-elk-billing
![Alt text](https://github.com/srajbr/aws-usage_billing-elk-dashboard/blob/master/screenshots/kibana_dashboard1.png?raw=true "Overview")
![Alt text](https://github.com/srajbr/aws-usage_billing-elk-dashboard/blob/master/screenshots/kibana_dashboard2.png?raw=true "Overview")

## Overview
 
 aws-elk-billing is a combination of configuration snippets and tools to assist with indexing AWS programatic billing access files(CSV's) and visualizing the data using Kibana. The entire process from getting data to visualization can be made automated with the docker architecture and some modification in respective script files.

### Primary Components
Task | Files or Process
------------ | -------------
Building the Docker Architecture and Starting all process | `Dockerfile`, `docker-compose.yml`
Configuration of Logstash | `logstash.conf`
Elasticsearch indexing template | `aws-billing-es-template.json`
Parsing the aws-billing CSV's and send them to logstash as JSON | `main.go`
Automated download latest zipped file from S3 bucket and extract the billing\_report\_csv file | `s3\_csv\_grab.py`
Kibana Dashboard Export in json format to get you started| `kibana_dashboard.json`

### The Base Architecture
There are Four Docker instances running throughout the entire visualization. 

1. Ealasticsearch Docker (image source: https://hub.docker.com/r/droidlabour/elasticsearch)
2. Kibana Docker (image source: https://hub.docker.com/r/droidlabour/kibana)
3. Logstash Docker (image source: https://hub.docker.com/r/droidlabour/logstash)
4. Aws-elk-billing Docker (localy build  image)

Each name is self-explanatory about the primary process they are running. If you want to find more about what and how this dockers are running go to the repository (https://github.com/PriceBoardIn) and you will find all the `Dockerfile` and `docker-compose.yml` files. Finally the Aws-elk-billing Docker takes care of all the othe Three docker running and this is the only docker you might want to modify (or might not also).

PS: Don't worry about the system being heavy with so many dockers, they run only one or two process So, its like 4 application running. But it has many benifits (docker user will know :p)

## Getting Started
Clone the Repository and make sure that no process is listning to the ports used by all these dockers.

Ports | Process
------------ | -------------
9200, 9300 | Elasticsearch
5160 | Kibana
5140 | Logstash

### Set S3 credentials
Create a file named `docker-compose.aws.prod-key.yml` with the following content and modify it with your S3 credentials
```
version: '2'
 services:
  env_var:
   environment:
    - ENV=prod
    - DEBIAN_FRONTEND=noninteractive
    - TERM=xterm
    - AWS_ACCESS_KEY_ID=---your_access_key---
    - AWS_SECRET_ACCESS_KEY=---your_secret_key---
    - S3_BUCKET_NAME=...your_bucket_name...
    - S3_BILL_PATH_NAME=/...pathname_without_ending_slash...
# follow the syntax, '/your_directory' and don't end with '/' , This path should have the
# monthly reports in child directory
```
This file is being extended by the `docker-compose.yml` in the root directory
In this way your credentials will not go to git even if you push any change

#### Run Docker
The entire process is automated through scripts and docker. All the components would be downloaded automatically inside your docker

First go to the repository root directory.

Run
`sudo docker-compose build .`

This command in the root directory of the Repository will start building the `Aws-elk-billing Docker` (4th) docker and this will make sure all the other Three dockers are build correctly.

Then Run 
`sudo docker-compose up -d`
To run all the dockers as demon process.
PS: remove the -d flag if you want to run as foreground process and get the running logs.

This process wil take sometime (downloading indexing and everything),

After that you can see `kibana` at `localhost:5601`

Make sure you change the time stamp from the upper-right corner of your kibana webapp to the time perioud you want to view the details.

I have provided a Demo Dashboard along with some visualization. Check it out and use it as referenec to build your own dashboard and visualization according to your need.

After you are done just do `sudo docker-compose down` to stop everything.

## Known Issues

* It will take time depending on your system and data, if you do excess querries before the docker process is done, it might crash. In that case jsut stop the docker with `sudo docker-compose down` and run again. You might also want to see the logs to know whats hapenning to escape this.
* The mapping template can be made stronger, that being said if the mapping is edited and something is not working the code will not throw error (in logs it will!), rather it will take up previous data (or something silly)
