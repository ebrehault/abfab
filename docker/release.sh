#!/bin/bash

docker build -f docker/Dockerfile-utils -t abfab-utils .
docker tag abfab-utils:latest ebrehault/abfab-utils:latest
docker push ebrehault/abfab-utils:latest

cd server/abfab
docker build -t abfab .
docker tag abfab:latest ebrehault/abfab:latest
docker push ebrehault/abfab:latest
cd -
