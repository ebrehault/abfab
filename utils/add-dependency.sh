#!/bin/bash

PASSWORD=$1
DEPENDENCY=$2

cd ..
mkdir tmp
cd tmp
npm install --prefix ./ $DEPENDENCY
mv ./node_modules ./libs
cd ..
for d in ./tmp/libs/*/ ; do
    python utils/sync.py up libs/`basename "$d"` --root tmp --auth root:$PASSWORD --host http://abfab:8080/db/app
done
rm -rf tmp
