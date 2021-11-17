#!/bin/bash

REPO=$1
BRANCH=$2
HOST=$3
PASSWORD=$4

cd ../src/$REPO
git switch $BRANCH
git pull -r origin $BRANCH
cd ../..
python utils/sync.py up $REPO --auth root:$PASSWORD --root ./src --host http://$HOST:8080/db/app --contents
