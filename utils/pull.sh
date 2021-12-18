#!/bin/bash

REPO=$1
BRANCH=$2
PASSWORD=$3

cd ../src/$REPO
git switch $BRANCH
git pull -r origin $BRANCH
cd ../..
python utils/sync.py up $REPO --auth root:$PASSWORD --root ./src --host http://abfab:8080/db/app --contents
