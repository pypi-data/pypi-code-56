from celery import Celery
import os
from .task_config import broker_transport_options

for key in broker_transport_options:
    if key.startswith('data_folder'):
        f = broker_transport_options[key]
        if not os.path.exists(f):
            os.makedirs(f)

app = Celery()
app.config_from_object('task_config')
