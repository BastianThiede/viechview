from BaseHTTPServer import HTTPServer
import base64
from SimpleHTTPServer import SimpleHTTPRequestHandler
from SocketServer import ThreadingMixIn
import os
import shutil
import ssl
import subprocess
import time
import json
from multiprocessing import Process
from gif_creator import GifCreator

PORT = 31337


class RequestHandler(SimpleHTTPRequestHandler):
    PIC_FOLDER = "viechview_pics"

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def create_day_folder_path(self):
        day_of_week = time.strftime("%A", time.gmtime())
        day_folder_name = os.path.join(RequestHandler.PIC_FOLDER, day_of_week)
        path = os.path.abspath(day_folder_name)
        if not os.path.isdir(path):
            os.makedirs(os.path.abspath(path))
        return path

    def create_folder_if_not_exists(self, folder_name):
        if not os.path.isdir(folder_name):
            os.makedirs(os.path.abspath(folder_name))

    def _handle_img(self, img, client_ip):
        human_readable_time = time.strftime("%d_%b_%Y_%H_%M_%S",
                                            time.gmtime())
        fname = ".".join([human_readable_time, 'jpg'])
        day_folder_path = self.create_day_folder_path()
        client_path = os.path.join(day_folder_path, client_ip)
        self.create_folder_if_not_exists(client_path)
        f_path = os.path.join(client_path, fname)
        with open(f_path, "wb") as f:
            f.write(base64.b64decode(img))
        print "Wrote File {} ".format(fname)

    def do_POST(self):
        self._set_headers()
        client_ip = self.client_address[0]
        self.data_string = self.rfile.read(int(self.headers['Content-Length']))
        data = json.loads(self.data_string)
        self._handle_img(data['img'], client_ip)

    def do_GET(self):
        os.chdir(os.path.join('..', 'client'))
        SimpleHTTPRequestHandler.do_GET(self)
        os.chdir(os.path.join('..', 'server'))


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""


if __name__ == '__main__':
    server = ThreadedHTTPServer(('', PORT), RequestHandler)
    server.socket = ssl.wrap_socket(server.socket, server_side=True,
                                    certfile='./server.pem')
    print 'Starting server on ' + str(PORT)
    server.serve_forever()
