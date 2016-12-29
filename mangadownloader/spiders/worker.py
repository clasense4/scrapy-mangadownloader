from __future__ import absolute_import, unicode_literals
from .celery import app
import logging

@app.task
def download(complete_image_url, local_image_path):
    # urllib.urlretrieve(complete_image_url, local_image_path)
    logging.info('Image saved to ' + local_image_path)
