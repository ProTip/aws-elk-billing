echo -e "POST /containers/awselkbilling_kibana_1/kill?signal=SIGKILL HTTP/1.0\r\n" | nc -U /var/run/docker.sock;
echo -e "POST /containers/awselkbilling_logstash_1/kill?signal=SIGKILL HTTP/1.0\r\n" | nc -U /var/run/docker.sock;
echo -e "POST /containers/awselkbilling_elasticsearch_1/kill?signal=SIGKILL HTTP/1.0\r\n" | nc -U /var/run/docker.sock;
