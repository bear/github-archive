#!/bin/bash
#
# Author: bear (Mike Taylor)
# License: MIT
# Copyright (c) 2014-2015 by Mike Taylor
#

CURDIR=`pwd`

if [ "$1" == "" ]; then
    echo "usage: archive.sh orgname reponame"
    exit
fi 
if [ "$2" == "" ]; then
    echo "usage: archive.sh orgname reponame"
    exit
fi 

echo "archiving $1/$2 into /tmp/$1_$2.tgz"

mkdir -p /tmp/archive
rm -rf /tmp/archive/$2.git
cd /tmp/archive

git clone --mirror git@github.com:$1/$2.git
python ${CURDIR}/archive.py -c ${CURDIR}/archive.cfg -o $1 -r $2 --issues
tar -czf $1_$2.tgz $2.git $2.json

echo "done"
