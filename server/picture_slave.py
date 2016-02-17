import subprocess
import uuid
import time
import os
import ftplib
import requests
import base64

def take_picture(picture_name, resolution='640x480'):
    """
    taking a webcam picture with fswebcam (so fswebcam has to be installed)
    It's simpler than OpvenCV / SimpleCV :D
    Args:
        picture_name: Name you want to use for your picture
        resolution: image resolution
    """
    # TODO : Figure out which options we actually need
    subprocess.check_call(['fswebcam', '-r',
                           resolution, picture_name,
                            '--no-banner'])
    with open(os.path.abspath(picture_name),'rb') as f:
        img_str =  base64.b64encode(f.read())

    os.remove(os.path.abspath(picture_name))
    return img_str
    


def date_filename(extension='jpg'):
    """
    Creating a filename with strftime date. Also adds a suffix
    Args:
        extension: file extension (default : jpg)
    Return:
        (str) date_string with extension

    """
    date_str = time.strftime("%d_%b_%Y_%H_%M_%S", time.gmtime())
    return ".".join([date_str, extension])


def setup_pictureslave(pic_interval=500, upload=False):
    """
    This Method will take ten thousand pictures every time pic_interval is
    passed. Each File is saved in a folder defined by PIC_FOLDER.
    Also manages uploading of File (currently only ftp)
    Args:
        pic_interval: interval between each camera picture (in s)
        upload: Flag if image should be uploaded
    """
    for _ in xrange(10000):
        f_name = date_filename()
        b64_encoded_img = take_picture(f_name)
        print b64_encoded_img
        requests.post("http://localhost:8080", json = {"img":b64_encoded_img})
        time.sleep(pic_interval)


if __name__ == "__main__":
    setup_pictureslave(10)

