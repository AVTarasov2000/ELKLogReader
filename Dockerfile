FROM openjdk:slim
COPY --from=python:3.6 / /

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