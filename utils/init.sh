#!/bin/bash

sleep 15
response=$(curl --write-out '%{http_code}' --silent --output /dev/null http://abfab:8080/db/app --user root:root)
if [ $response != '200' ]; then
    curl -i -X POST http://abfab:8080/db/ -H 'Accept: application/json' -H 'Content-Type: application/json' --data-raw '{"@type": "Container", "description": "AbFab container", "id": "app", "title": "AbFabApp"}' --user root:root
    python sync.py up libs --auth root:root --root .
    python sync.py up abfab --auth root:root --root ./client
fi