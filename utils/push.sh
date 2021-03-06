#!/bin/bash

REPO=$1
BRANCH=$2
PASSWORD=$3
COMMIT=$4

cd ../src/$REPO
git config --global user.email "AbFab"
git config --global user.name "AbFab"
git switch $BRANCH 2>/dev/null || git switch -c $BRANCH
python ../../utils/sync.py down $REPO --auth root:$PASSWORD --root .. --host http://abfab:8080/db/app --contents
git add .
git commit -m "$COMMIT"
git push origin $BRANCH
