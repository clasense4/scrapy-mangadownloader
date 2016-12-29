from __future__ import absolute_import, unicode_literals
from celery import Celery

app = Celery(broker='redis://localhost:6379/0', 
    include=['mangadownloader.spiders.worker']
    )

if __name__ == '__main__':
    app.start()
