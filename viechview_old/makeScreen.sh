#!/bin/sh
SCREENPATH=$(pwd)"/screens/"
INTERVAL=$(($1*60))
while true;
	do streamer -o /tmp/tmp.ppm &> /dev/null;
	DAY=$(date +"%a")
	TIMEOFDAY=$(date +"%X")
	TIMESTAMP=$DAY$TIMEOFDAY
	FILEPATH="$SCREENPATH""$TIMESTAMP"".jpg"
	sleep 2;
	ppmtojpeg /tmp/tmp.ppm > $FILEPATH;	
	echo $FILEPATH" written";
#	HASH = $(shasum $FILEPATH | head -c 40);
	redis-cli -x set $TIMESTAMP < $FILEPATH &
	redis-cli rpush $DAY $TIMEOFDAY &
	sleep $(($INTERVAL - 2));
done;
