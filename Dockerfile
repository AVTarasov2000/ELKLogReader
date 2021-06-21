#FROM python:3.6-alpine
##FROM openjdk:slim
#FROM ubuntu:14.04
FROM picoded/ubuntu-base
#COPY --from=openjdk:8 / /
#


# This is in accordance to : https://www.digitalocean.com/community/tutorials/how-to-install-java-with-apt-get-on-ubuntu-16-04
RUN apt-get update && \
	apt-get install -y openjdk-8-jdk && \
	apt-get install -y ant && \
	apt-get clean && \
	rm -rf /var/lib/apt/lists/* && \
	rm -rf /var/cache/oracle-jdk8-installer;

# Fix certificate issues, found as of
# https://bugs.launchpad.net/ubuntu/+source/ca-certificates-java/+bug/983302
RUN apt-get update && \
	apt-get install -y ca-certificates-java && \
	apt-get clean && \
	update-ca-certificates -f && \
	rm -rf /var/lib/apt/lists/* && \
	rm -rf /var/cache/oracle-jdk8-installer;

# Setup JAVA_HOME, this is useful for docker commandline
ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64/


RUN groupadd -g 1000 elasticsearch && useradd elasticsearch -u 1000 -g 1000

RUN apt-key adv --keyserver pgp.mit.edu --recv-keys 46095ACC8548582C1A2699A9D27D666CD88E42B4 && \
    add-apt-repository -y "deb http://packages.elastic.co/elasticsearch/2.x/debian stable main" --keyserver https://pgp.mit.edu/ && \
    apt-get update && \
    apt-get install -y --no-install-recommends elasticsearch

WORKDIR /usr/share/elasticsearch

#RUN set -ex && for path in data logs config config/scripts; do \
#        mkdir -p "$path"; \
#        chown -R elasticsearch:elasticsearch "$path"; \
#    done

COPY elasticsearch.yml /usr/share/elasticsearch/config/



USER elasticsearch

ENV PATH=$PATH:/usr/share/elasticsearch/bin

CMD ["elasticsearch"]

EXPOSE 9200 9300




#RUN apk add --no-cache python3 \
#&& python3 -m ensurepip \
#&& pip3 install --upgrade pip setuptools \
#&& rm -r /usr/lib/python*/ensurepip && \
#if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
#if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
#rm -r /root/.cache
#
#### Get Flask for the app
#RUN pip install --trusted-host pypi.python.org flask


#RUN adduser -D logreader
#
#WORKDIR /home/logreader
#
#COPY requirements.txt requirements.txt
#RUN python -m venv venv
#RUN venv/bin/pip install -r requirements.txt
#RUN venv/bin/pip install waitress
#
#COPY app app
#COPY logreader.py boot.sh ./
#RUN chmod +x boot.sh
#
#ENV FLASK_APP logreader.py
#
#RUN chown -R logreader:logreader ./
#USER logreader
#
#EXPOSE 5000
#ENTRYPOINT ["./boot.sh"]