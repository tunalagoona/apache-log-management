FROM ubuntu:18.04

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

WORKDIR /package

RUN apt-get update && apt-get install -y python3 python3-pip

COPY apache_log_manager apache_log_manager
RUN pip3 install -r apache_log_manager/requirements.txt
