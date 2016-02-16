import os
import posixpath
import urllib
import sys
import json
from redis import Redis
import BaseHTTPServer

PATH = "/tmp/screens"
redis = Redis()

def getImage(ctx):
	key = ctx.path[5:]
	content = redis.get(key)
	if content:	
		ctx.send_response(200)
		mime = "image/jpg"
		ctx.send_header("Content-Type", "%s; encoding=UTF-8" % mime)
		ctx.end_headers()
		ctx.wfile.write(content)
	else:
		ctx.send_response(404)
		ctx.end_headers()

def listImages(ctx):
	(day, min, max) = ctx.path[6:].split("/")
	ctx.send_response(200)
	mime = "application/json"
	ctx.send_header("Content-Type", "%s; encoding=UTF-8" % mime)
	ctx.send_header("Access-Control-Allow-Origin", "*")
	ctx.end_headers()
	ctx.wfile.write(json.dumps(redis.lrange(day,min,max)))

routes = {
	'/key': getImage,
	'/list': listImages
}

class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
	def do_GET(self, *args):
		for route, func in routes.items():
			if self.path.startswith(route):
				return func(self)
		self.send_response(404)
		self.end_headers()
if __name__ == '__main__':
	BaseHTTPServer.test(RequestHandler, BaseHTTPServer.HTTPServer)
