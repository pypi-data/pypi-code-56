import json
from typing import Any, Dict

import boto3

import botocore

from jeffy.sdk import SdkBase


class Sqs(SdkBase):
    """SQS Client."""

    _resource = None

    @classmethod
    def get_resource(self) -> botocore.client.BaseClient:
        """
        Get boto3 client for SQS.

        Usage::
            >>> from jeffy.sdk.sqs import Sqs
            >>> Sqs.get_resource().send_message(...)
        """
        if Sqs._resource is None:
            Sqs._resource = boto3.client('sqs')
        return Sqs._resource

    def send_message(
        self,
        message: Any,
        queue_url: str,
        correlation_id: str = ''
    ) -> Dict:
        """
        Send message to SQS Queue with correlationid.

        Usage::
            >>> from jeffy.sdk.sqs import Sqs
            >>> Sqs().send_message(...)
        """
        if correlation_id == '':
            correlation_id = self.app.correlation_id
        return self.get_resource().send_message(
            QueueUrl=queue_url,
            MessageBody=json.dumps({
                self.app.correlation_attr_name: correlation_id,
                'item': message
            })
        )
