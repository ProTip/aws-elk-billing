#!/bin/bash

# Default search mapping for dashboard to work
curl -XPUT "http://elasticsearch:9200/.kibana/_mappings/search" -d "`cat discover_search.json`"

# Creating index and adding specific mapping for gCloud dashboard to work
curl -XPUT 'elasticsearch:9200/gcloud_billing?pretty' -H 'Content-Type: application/json' -d "`cat gCloud-mappings.json`"