#!/bin/bash

cd `dirname $0`

pid=`ps x | grep "say_from_dm.py" | grep "buaatreeholes" | grep -v grep | awk '{ print $1; }'`
echo "$pid"
kill $pid 2>/dev/null

python say_from_dm.py >> data/say_from_dm.log 2>&1 &
