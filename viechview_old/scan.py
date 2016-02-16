from redis import Redis
import os
from hashlib import sha1

redis = Redis()
order = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]

for day in order:
	redis.delete(day)

dirlist = os.listdir("screens")
ret = []
tmp = {}
for pic in dirlist:
	(day, timestamp) = (pic[:3], pic[3:11])
	if day not in tmp:
		tmp[day] = [timestamp]
	else:
		tmp[day].append(timestamp)
for day in order:
	if day in tmp:
		tmp[day].sort()
		for ts in tmp[day]:
			fileid = "%s%s" % (day, ts)
			f = open("screens/%s.jpg" % fileid)	
			content = f.read()
			redis.set(fileid, content)
			redis.rpush(day, ts)
		print "added %s" % day
