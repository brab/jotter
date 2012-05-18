#!/bin/bash

git pull
. ~/.virtualenvs/jotter/bin/activate
./manage.py migrate
