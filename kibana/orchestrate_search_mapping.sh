#!/bin/bash

# Default search mapping for dashboard to work
curl -XPUT "http://elasticsearch:9200/.kibana/_mappings/search" -d "`cat discover_search.json`"
