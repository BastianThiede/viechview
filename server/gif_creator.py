import base64
import os
import shutil
import subprocess
import time


class GifCreator(object):
    def __init__(self):
        super(GifCreator,self).__init__()
	self.pics_needed = 10
	self.check_interval = 10

    def create_day_folder_path(self):
        day_of_week = time.strftime("%A", time.gmtime())
	day_folder_name = os.path.join("viechview_pics", day_of_week)
	path = os.path.abspath(day_folder_name)
	if not os.path.isdir(path):
            os.makedirs(os.path.abspath(path))
	return path

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

    def find_gif_rdy_folders(self):
        while True:
                day_folder_path = self.create_day_folder_path()
                print "Checking: {}".format(day_folder_path)
		folder_paths = [os.path.join(day_folder_path,folder) for folder 
		        in os.listdir(day_folder_path) if os.path.isdir(os.path.join(day_folder_path,folder))]
                print folder_paths
		full_folder_paths = [directory for directory in folder_paths if len(self.list_filenames_in_folder(directory)) > self.pics_needed]
                print full_folder_paths
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
		time.sleep(self.check_interval)

if __name__ == '__main__':
    giffer = GifCreator()
    giffer.find_gif_rdy_folders()
