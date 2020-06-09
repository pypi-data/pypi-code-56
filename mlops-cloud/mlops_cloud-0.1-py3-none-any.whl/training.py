import os
import boto3
import ast
import argparse
import json
from datetime import datetime
from uuid import uuid4

AWS_REGION = os.environ["AWS_REGION"]
ALLOWED_FRAMEWORKS = ["tensorflow", "scikit", "pytorch"]


class Trainer:
    def __init__(self, framework: str):
        self.args = self._parse_args()
        self.framework = framework
        self.job_id = self.args["model_id"]
        self.project_id = self.args["project_id"]
        self.metrics = self.args["metrics"]
        if self.framework not in ALLOWED_FRAMEWORKS:
            raise Exception(f"Allowed frameworks are {ALLOWED_FRAMEWORKS}.")
        if self.framework == "tensorflow":
            from metrics import MLOpsTensorFlowCallback

            self.tf_callback = MLOpsTensorFlowCallback(
                self.metrics, self.job_id, self.project_id
            )

    def infer(self, s):
        """ Tries to infer the type of an input variable _s_ or fails and defaults to string.
        """
        try:
            val = ast.literal_eval(s)
        except Exception:
            return str(s)
        acceptable_types = (int, str, float)
        if any(isinstance(val, x) for x in acceptable_types):
            return val

    def _find_hyperparameters(self) -> list:
        """ Parses a string of hyperparameters like: epochs,batch_size
        and returns them as a list. This list is passed from the CreateTrainingJob.
        """
        parser = argparse.ArgumentParser()
        parser.add_argument("hps_to_parse", type=str)
        args = parser.parse_known_args()
        return vars(args[0])["hps_to_parse"].split(",")

    def _parse_args(self) -> dict:
        """ Parses all arguments, including the unknown, varying input hyperparameters.
        All arguments from the Sagemaker estimator to the training container are passed as command line args.
        """
        hps_to_parse = self._find_hyperparameters()
        parser = argparse.ArgumentParser()
        for hp in hps_to_parse:
            parser.add_argument(f"--{hp}")

        parser.add_argument(
            "--train", type=str, default=os.environ.get("SM_CHANNEL_TRAIN")
        )
        parser.add_argument(
            "--test", type=str, default=os.environ.get("SM_CHANNEL_TEST")
        )
        parser.add_argument(
            "--val", type=str, default=os.environ.get("SM_CHANNEL_VALIDATION")
        )
        parser.add_argument("--model_dir", type=str)
        parser.add_argument(
            "--sm-model-dir", type=str, default=os.environ.get("SM_MODEL_DIR")
        )
        parser.add_argument(
            "--hosts", type=list, default=json.loads(os.environ.get("SM_HOSTS"))
        )
        parser.add_argument(
            "--current-host", type=str, default=os.environ.get("SM_CURRENT_HOST")
        )
        arguments = vars(parser.parse_known_args())
        for k, v in arguments.items():
            arguments[k] = self.infer(v)
        arguments["metrics"] = arguments["metrics"].split(",")
        return arguments

    def save_scikit(self, model, model_dir):
        import sklearn
        from joblib import dump

        dump(model, os.path.join(model_dir, "model.joblib"))

    def save_pytorch(self, model, model_dir: str):
        import torch

        with open(os.path.join(model_dir, "model.pth"), "wb") as f:
            torch.save(model.state_dict(), f)

    def save_tensorflow(self, model, model_dir):
        import tensorflow as tf

        model.save(os.path.join(model_dir, "model.pth"))
