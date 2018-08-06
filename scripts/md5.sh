#!usr/bin bash
tail -n +2 $1 | tr -d '\n' | md5sum