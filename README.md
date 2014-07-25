# aws-elk-billing
 
## Overview
 
 aws-elk-billing is a combination of configuration snippets and tools to assist with indexing AWS programatic billing access files(CSV's) and visualizing the data using Kibana.

### Primary Components

 * Logstash config
 * Elasticsearch index template
 * `aws-billing` The command line tool to parse billing CSV's and send them to logstash as JSON
 * Kibana dashboards in JSON format to get you started

## Getting Started

Install logstash.  This is not an elasticsearch tutorial so we'll be using the embedded elasticsearch option.  In fact, I use this as well because it's easy and not a critical component.  I would recommend using the APT or YUM repositories if that suites your distro: http://logstash.net/docs/1.4.2/repositories .

Install apache2.  Ensure mod_proxy, mod_proxy_http, and mod_ssl are enabled.  Give the example config `kibana-vhost.conf` a go, replacing `example.com` with your host name.

Install Kibana

Place the provided `logstash.conf` in the appropriate location(e.g. `/etc/logstash/conf.d/logstash.conf`).  Alternatively, merge the relevant bits into your logstash configuration.

Add the provided elasticsearch index template `aws-billing-es-template.json`:
````
curl -XPUT localhost:9200/_template/aws_billing -d "`cat aws-billing-es-template.json`"
````
This template mostly mirrors the logstash template but matches the aws-billing indexes.  Restart logstash.

Download all of your detailed billing files into `some directory`.  Build the golang program or grab the provided linux amd64 binary release: https://github.com/ProTip/aws-elk-billing/releases .  You're ready to import. Change to `some directory` and bring the aws-billing executable in:
````
ls *.csv | xargs -I'{}' ./aws-billing --file {} --concurrency 1
````
Setting concurrency higher will use more cores but most likely logstash/elasticsearch will be your bottleneck.  This can take a while; the program will print the number of records it has processed every 10k records.
