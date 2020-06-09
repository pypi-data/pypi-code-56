import boto3
import os
from datetime import datetime
from uuid import uuid4
import json
import torch

from .training import TrainingBase

AWS_REGION = os.environ["AWS_REGION"]


class PyTorchTrainer(TrainingBase):
    def __init__(self):
        super().__init__()

    def save_pytorch(self, model, model_dir: str):
        with open(os.path.join(model_dir, "model.pth"), "wb") as f:
            torch.save(model.state_dict(), f)
