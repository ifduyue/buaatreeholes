#!/bin/bash

cd `dirname $0`

pid=`ps x | grep "say_from_dm.py" | grep "buaatreeholes" | grep -v grep | awk '{ print $1; }'`
if [ -z "$pid" ];then
./dm_restart.sh
fi
