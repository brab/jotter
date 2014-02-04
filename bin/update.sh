#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )";
cd "$DIR";
cd ..;
branch=$1;
if [ -z "branch" ]
then
    branch="master";
fi
git checkout "$branch";
git pull;
python3.3 server/manage.py migrate;
