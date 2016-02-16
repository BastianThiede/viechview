#!/bin/sh
SCREENPATH=$(pwd)"/screens/"
redis-cli del queue
for FILE in $(find $SCREENPATH -name "*.jpg");
	do NAME=$(basename $FILE | head -c 11);
	redis-cli -x set $NAME < $FILE;
	redis-cli rpush queue $NAME;
done;
