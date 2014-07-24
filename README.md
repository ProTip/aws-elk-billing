# aws-elk-billing
 
## Overview
 
 aws-elk-billing is a combination of configuration snippets and tools to assist with indexing AWS programatic billing access files(CSV's) and visualizing the data using Kibana.

### Primary Components

 * Logstash config
 * Elasticsearch index template
 * `aws-billing` The command line tool to parse billing CSV's and send them to logstash as JSON
 * Kibana dashboards in JSON format to get you started

## Getting Started

Install logstash.  This is not an elasticsearch tutorial so we'll be using the embedded elasticsearch option.  In fact, I use this as well because it's easy and not a critical component.
