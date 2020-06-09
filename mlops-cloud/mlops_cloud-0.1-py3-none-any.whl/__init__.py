from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from datetime import datetime
import boto3
import argparse
import os
import json


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--epochs", type=int, default=1)
    parser.add_argument("--batch_size", type=int, default=64)
    parser.add_argument("--learning_rate", type=float, default=0.1)
    parser.add_argument("--model_id", type=str)
    parser.add_argument("--project_id", type=str)
    parser.add_argument("--train", type=str, default=os.environ.get("SM_CHANNEL_TRAIN"))
    parser.add_argument("--test", type=str, default=os.environ.get("SM_CHANNEL_TEST"))
    parser.add_argument(
        "--validation", type=str, default=os.environ.get("SM_CHANNEL_VALIDATION")
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
    return vars(parser.parse_known_args())


def init():
    parameters = _parse_args()
