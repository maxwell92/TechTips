#! /bin/bash

STR=""

if [ -n "$STR" ]   # -n, if str is null, return 0
then
    echo $STR
    echo "not null"
else
    echo $STR
    echo "null"
fi

