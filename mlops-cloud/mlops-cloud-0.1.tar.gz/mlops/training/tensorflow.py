import boto3
import os
from datetime import datetime
from uuid import uuid4
import json
import tensorflow as tf

from .training import TrainingBase

AWS_REGION = os.environ["AWS_REGION"]

METRICS_MAP = {
    "auc": tf.keras.metrics.AUC(),
    "rmse": tf.keras.metrics.RootMeanSquaredError(),
    "accuracy": tf.keras.metrics.Accuracy(),
    "fp": tf.keras.metrics.FalsePositives(),
    "tp": tf.keras.metrics.TruePositives(),
    "fn": tf.keras.metrics.FalseNegatives(),
    "tn": tf.keras.metrics.TrueNegatives(),
    "precision": tf.keras.metrics.Precision(),
    "recall": tf.keras.metrics.Recall(),
}


class MLOpsCallback(tf.keras.callbacks.Callback):
    def __init__(self, metrics: list, model_id: str, project_id: str):
        self.sqs = boto3.client("ssm", region_name=AWS_REGION)
        self.sqs_url = self._get_sqs_url()
        self.metrics = metrics
        self.tf_metrics = [METRICS_MAP[x] for x in self.metrics]
        self.model_id = model_id
        self.project_id = project_id

    def _get_sqs_url(self):
        return self.sqs.get_parameter(
            Name="mlops-sqs-metrics-url", WithDecryption=True
        )["Parameter"]["Value"]

    def on_epoch_end(self, epoch, logs={}):
        data = {}
        for metric in self.metrics:
            data[metric] = logs[metric].item()
            data[f"val_{metric}"] = logs[f"val_{metric}"].item()

        self.save_metrics(data)

    def on_train_end(self, logs={}):
        print(f"train end log: {logs}")

    def save_metrics(self, data: dict):
        """ Push metrics to a FIFO SQS queue.
        _data_ has the expected format of {'metric': 'value'}
        """
        time = datetime.now()
        entries = []
        msg_group_id = uuid4().int
        for k, v in data.items():
            msg_dedup_id = uuid4().int
            msg_id = uuid4().int
            entry = {
                "Id": msg_id,
                "MessageBody": json.dumps(
                    {
                        "data": {
                            "metric": k,
                            "value": v,
                            "timestamp": time.isoformat(),
                        },
                        "type": "sagemaker",
                        "tenantId": 123,
                        "modelId": self.model_id,
                        "projectId": self.project_id,
                    }
                ),
                "MessageDeduplicationId": msg_dedup_id,
                "MessageGroupId": msg_group_id,
            }
            entries.append(entry)
        self.sqs.send_message_batch(QueueUrl=self.sqs_url, Entries=entries)


class TensorFlowTrainer(TrainingBase):
    def __init__(self):
        super().__init__()
        self.callback = MLOpsCallback(self.metrics, self.model_id, self.project_id)
        print("---- ARGS ----")
        print(self.args)

    def save_model(self, model):
        model.save(os.path.join(self.args["sm_model_dir"], "model.tf"))
