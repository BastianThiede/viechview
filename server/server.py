from BaseHTTPServer import HTTPServer
import base64
from SimpleHTTPServer import SimpleHTTPRequestHandler
import os
import shutil
import ssl
import subprocess
import time
import json

PORT = 31337


class RequestHandler(SimpleHTTPRequestHandler):
    PIC_FOLDER = "viechview_pics"
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def _get_last_date_fname(self,file_names,extension='gif'):
        # lol \o/
         return time.strftime('%d_%b_%Y_%H_%M_%S', sorted([time.strptime(date_str.split('.')[0], "%d_%b_%Y_%H_%M_%S") for date_str in file_names], reverse=True)[0])
    
    def _fname_to_timestamp(self,fname):
        return time.strptime(fname.split('.')[0], "%d_%b_%Y_%H_%M_%S")

    def list_filenames_in_folder(self,path,extension='.jpg'):
        return [file_name for file_name in os.listdir(path) if file_name.endswith(extension)]
    
    def create_folder_if_not_exists(self,folder_name):
        if not os.path.isdir(folder_name):
            os.makedirs(os.path.abspath(folder_name))


    def _handle_img(self, img,client_ip):
        human_readable_time = time.strftime("%d_%b_%Y_%H_%M_%S",
                                            time.gmtime())
        day_of_week = time.strftime("%A", time.gmtime())
        day_folder_name = os.path.join(self.PIC_FOLDER, day_of_week)
        fname = ".".join([human_readable_time, 'jpg'])
        day_folder_path = os.path.abspath(day_folder_name)
        client_path = os.path.join(day_folder_path,client_ip)
        self.create_folder_if_not_exists(client_path)
        f_path = os.path.join(client_path, fname)
        with open(f_path, "wb") as f:
            f.write(base64.b64decode(img))
        print "Wrote File {} ".format(fname)
        folder_paths = [os.path.join(day_folder_path,folder) for folder 
                in os.listdir(day_folder_path) if os.path.isdir(os.path.join(day_folder_path,folder))]
        full_folder_paths = [directory for directory in folder_paths if len(self.list_filenames_in_folder(directory)) > 100]
        for abs_path in full_folder_paths:
                new_pictures = self.list_filenames_in_folder(abs_path)
                last_date = self._get_last_date_fname(new_pictures)
                gif_name = "giffed_pic_until_{last_date}.gif".format(last_date=last_date)
                wildcard = os.path.join(abs_path,"*.jpg")
                subprocess.check_call(['convert', '-delay', '20', '-loop', 
                                       '0',wildcard, os.path.join(abs_path,gif_name)])
                used_pic_folder = 'used_pictures'
                processed_pictures_path = os.path.join(abs_path,used_pic_folder)
                self.create_folder_if_not_exists(processed_pictures_path)
                for pic in new_pictures:
                    file_destination  = os.path.join(abs_path,pic)
                    shutil.move(file_destination,processed_pictures_path)

    def do_POST(self):
        self._set_headers()
        client_ip =  self.client_address[0]
        self.data_string = self.rfile.read(int(self.headers['Content-Length']))
        data = json.loads(self.data_string)
        self._handle_img(data['img'],client_ip)

    def do_GET(self):
        os.chdir(os.path.join('..', 'client'))
        SimpleHTTPRequestHandler.do_GET(self)
        os.chdir(os.path.join('..', 'server'))

if __name__ == '__main__':
    server = HTTPServer(('', PORT), RequestHandler)
    server.socket = ssl.wrap_socket(server.socket, server_side=True,
                                    certfile='./server.pem')

    print 'Starting server on ' + str(PORT)
    server.serve_forever()
