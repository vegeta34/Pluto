#!/bin/bash

echo testid:${TESTID}
echo deviceid:${DEVICEID}
echo package:${PKGNAME}
echo version:1.0.0

url="http://10.12.236.236:8082/end/session?testid=${TESTID}&deviceid=${DEVICEID}&package=${PKGNAME}&version=1.0.0"
echo url:$url
wget -T 2 -t 1 $url -O end_session.json