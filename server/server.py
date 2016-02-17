from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
import ssl
import os
import time
import base64
import json

PORT = 31337


class RequestHandler(SimpleHTTPRequestHandler):
    PIC_FOLDER = "viechview_pics"

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def _handle_img(self, img):
        human_readable_time = time.strftime("%d_%b_%Y_%H_%M_%S",
                                            time.gmtime())
        day_of_week = time.strftime("%A", time.gmtime())
        day_folder_name = os.path.join(self.PIC_FOLDER, day_of_week)
        if not os.path.isdir(day_folder_name):
            os.makedirs(os.path.abspath(day_folder_name))
        fname = ".".join([human_readable_time, 'jpg'])
        f_path = os.path.join(day_folder_name, fname)
        with open(f_path, "wb") as f:
            f.write(base64.b64decode(img))
        print "Wrote File"

    def do_POST(self):
        self._set_headers()
        self.data_string = self.rfile.read(int(self.headers['Content-Length']))
        data = json.loads(self.data_string)
        self._handle_img(data['img'])

    def do_GET(self):
        os.chdir(os.path.join('..', 'client'))
        SimpleHTTPRequestHandler.do_GET(self)
        os.chdir(os.path.join('..', 'server'))

if __name__ == '__main__':
    server = HTTPServer(('', PORT), RequestHandler)
    server.socket = ssl.wrap_socket(server.socket, server_side=True,
                                    certfile='furfm.cert', keyfile='furfm.key')

    print 'Starting server on ' + str(PORT)
    server.serve_forever()
