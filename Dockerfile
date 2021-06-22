FROM python:3.6-alpine

RUN adduser -D logreader

WORKDIR /home/logreader

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install waitress

COPY app app
COPY logreader.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP logreader.py

RUN chown -R logreader:logreader ./
USER logreader

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]


#docker run --name elasticsearch -d -p 9200:9200 -p 9300:9300 --rm -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch-oss:6.1.1
#docker run logreader -d -p 8000:5000 --link elasticsearch:elasticsearch -e ELASTICSEARCH_URL=http://elasticsearch:9200

#docker run --name elasticsearch --net my_net -p 9200:9200 -p 9300:9300 --rm -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.13.2 elasticsearch
#docker run --name lr -d -p 8000:5000 --rm --link elasticsearch:elasticsearch -e ELASTICSEARCH_URL=http://elasticsearch:9200 logreader
#docker run --name logreader --rm -d -p 8000:5000 --link elasticsearch:elasticsearch -e ELASTICSEARCH_URL=http://elasticsearch:9200 logreader
