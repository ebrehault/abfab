#!/bin/bash

PASSWORD=$1

sleep 15
response=$(curl --write-out '%{http_code}' --silent --output /dev/null http://abfab:8080/db/app --user root:$PASSWORD)
if [ $response != '200' ]; then
    curl -i -X POST http://abfab:8080/db/ -H 'Accept: application/json' -H 'Content-Type: application/json' --data-raw '{"@type": "Container", "description": "AbFab container", "id": "app", "title": "AbFabApp"}' --user root:$PASSWORD
    python utils/sync.py up libs --auth root:$PASSWORD --root . --host http://abfab:8080/db/app
    curl -i -X POST http://abfab:8080/db/app/libs/@sharing -H 'Accept: application/json' -H 'Content-Type: application/json' --data-raw '{"prinrole": [{"principal": "Anonymous User", "role": "guillotina.Reader", "setting": "AllowSingle"}]}' --user root:$PASSWORD
    python utils/sync.py up abfab --auth root:$PASSWORD --root ./client --host http://abfab:8080/db/app
    curl -i -X POST http://abfab:8080/db/app/abfab/@sharing -H 'Accept: application/json' -H 'Content-Type: application/json' --data-raw '{"prinrole": [{"principal": "Anonymous User", "role": "guillotina.Reader", "setting": "AllowSingle"}]}' --user root:$PASSWORD
fi

cd utils
flask run --host=0.0.0.0
