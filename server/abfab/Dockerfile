FROM python:3.9.5

WORKDIR /app

RUN pip install guillotina

COPY . .

RUN python setup.py develop