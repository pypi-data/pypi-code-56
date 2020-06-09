import boto3
import os
from datetime import datetime
from uuid import uuid4
import json
import sklearn
from joblib import dump

from .training import TrainingBase

AWS_REGION = os.environ["AWS_REGION"]


class SciKitTrainer(TrainingBase):
    def __init__(self):
        super().__init__()

    def save_scikit(self, model, model_dir):
        dump(model, os.path.join(model_dir, "model.joblib"))
