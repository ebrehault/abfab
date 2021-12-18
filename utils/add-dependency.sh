#!/bin/bash

PASSWORD=$1
DEPENDENCY=$2

mkdir tmp
cd tmp
npm install --prefix ./ $DEPENDENCY
mv ./node_modules ./libs
for d in ./libs/*/ ; do
    python ../sync.py up libs/`basename "$d"` --auth root:$PASSWORD --host http://abfab:8080/db/app
done
cd ..
rm -rf tmp
