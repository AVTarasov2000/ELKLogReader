docker run --name elasticsearch -d -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.13.2
docker run --name logreader --rm -d -p 8000:5000 --link elasticsearch:elasticsearch -e ELASTICSEARCH_URL=http://localhost:9200 logreader
#docker run --rm -d -it -v ~/config/:\c\Users\avtarasov\PycharmProjects\ELKLogReader\logstash_configs\logstashConfig docker.elastic.co/logstash/logstash:7.13.2
