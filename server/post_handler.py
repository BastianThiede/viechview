import base64
from BaseHTTPServer import BaseHTTPRequestHandler
import os
import time


import simplejson

class PostHandler(BaseHTTPRequestHandler):
    PIC_FOLDER = "viechview_pics"
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def _handle_img(self,img):
        human_readable_time = time.strftime("%d_%b_%Y_%H_%M_%S",
                                            time.gmtime())
        day_of_week = time.strftime("%A",time.gmtime())
        day_folder_name = os.path.join(self.PIC_FOLDER,day_of_week)
        if not os.path.isdir(day_folder_name):
            os.makedirs(os.path.abspath(day_folder_name))
        fname = ".".join([human_readable_time, 'jpg'])
        f_path = os.path.join(day_folder_name,fname)
        with open(f_path,"wb") as f:
            f.write(base64.b64decode(img))
        print "Wrote File"


    def do_POST(self):
        self._set_headers()
        self.data_string = self.rfile.read(int(self.headers['Content-Length']))
        data = simplejson.loads(self.data_string)
        self._handle_img(data['img'])


if __name__ == '__main__':
    from BaseHTTPServer import HTTPServer
    server = HTTPServer(('localhost', 8080), PostHandler)
    print 'Starting server, use <Ctrl-C> to stop'
    server.serve_forever()
