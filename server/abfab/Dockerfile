FROM python:3.9.5-slim-buster

WORKDIR /app
LABEL name="AbFab" \
    description="Absolutely fabulous web application publication environment" \
    maintainer="Eric BREHAULT"

ENV LANG C.UTF-8
ENV LANGUAGE C.UTF-8
ENV LC_ALL C.UTF-8

RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
	locales git-core gcc g++ netcat libxml2-dev \
    	libxslt-dev libz-dev python3-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install guillotina

COPY . .

RUN python setup.py develop