import os
import boto3
import ast
import argparse
import json
from datetime import datetime
from uuid import uuid4
import fastparquet
import pandas as pd
import numpy as np


AWS_REGION = os.environ["AWS_REGION"]
ALLOWED_FRAMEWORKS = ["tensorflow", "scikit", "pytorch"]


class TrainingBase:
    def __init__(self):
        self.args = self._parse_args()
        self.model_id = self.args["model_id"]
        self.project_id = self.args["project_id"]
        self.metrics = self.args["metrics"]

    def infer_type(self, s):
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
        for k, v in arguments[0].items():
            arguments[k] = self.infer_type(v)
        arguments["metrics"] = arguments["metrics"].split(",")
        return arguments

    def _read_csv(self, path: str) -> pd.DataFrame:
        files = [x for x in os.listdir(path) if "run" in x]
        li = []
        for file in files:
            df = pd.read_csv(file, index_col=None, header=0)
            li.append(df)

        return pd.concat(li, axis=0, ignore_index=True)

    def _read_parquet(self, path: str, columns=None) -> pd.DataFrame:
        return pd.read_parquet(path, columns=columns)

    def _split_data_label(self, df, label_indexes) -> (np.array, np.array):
        _, cols = df.shape
        labels = df.iloc[:, label_indexes].to_numpy().reshape(-1, len(label_indexes))
        # Labels at end columns
        if label_indexes[-1] == cols:
            data = (
                df.iloc[:, range(0, cols - labels.shape[1])]
                .to_numpy()
                .reshape(-1, cols - labels.shape[1])
            )
        # Lables at beginning
        else:
            data = (
                df.iloc[:, range(labels.shape[1], cols)]
                .to_numpy()
                .reshape(-1, cols - labels.shape[1])
            )
        return data, labels

    def read_data(
        self, label_indexes: list, data_format: str = "parquet"
    ) -> dict(str, np.array):
        if self.args["train"] is not None:
            df = (
                self._read_parquet(self.args["train"])
                if data_format == "parquet"
                else self._read_csv(self.args["train"])
            )
            self.train_data, self.train_labels = self._split_data_label(
                df, label_indexes
            )
            print(
                f"Shape of training data: {self.train_data.shape}, labels: {self.train_labels.shape}"
            )
        if self.args["val"] is not None:
            df = (
                self._read_parquet(self.args["val"])
                if data_format == "parquet"
                else self._read_csv(self.args["val"])
            )
            self.val_data, self.val_labels = self._split_data_label(df, label_indexes)
            print(
                f"Shape of validation data: {self.val_data.shape}, labels: {self.val_labels.shape}"
            )
        if self.args["test"] is not None:
            df = (
                self._read_parquet(self.args["test"])
                if data_format == "parquet"
                else self._read_csv(self.args["test"])
            )
            self.test_data, self.test_labels = self._split_data_label(df, label_indexes)
            print(
                f"Shape of test data: {self.test_data.shape}, labels: {self.test_labels.shape}"
            )
