#!/bin/bash

cd `dirname $0`

pid=`ps x | grep "python buaatreeholes_web.py" | grep -v grep | awk '{ print $1; }'`
echo "$pid"
kill $pid 2>/dev/null

for i in $@; do
    python buaatreeholes_web.py $i>> data/err 2>&1 &
done
