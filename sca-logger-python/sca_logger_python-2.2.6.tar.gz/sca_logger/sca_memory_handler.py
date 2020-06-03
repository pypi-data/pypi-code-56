import gzip
import io
import json
import logging
import os
from io import BytesIO
from logging.handlers import MemoryHandler

from sca_logger import utils

KINESIS_SCA_LOG_STREAM = os.environ['KINESIS_SCA_LOG_STREAM']
MEMORY_HANDLER_LOG_CAPACITY = int(os.getenv('MEMORY_HANDLER_LOG_CAPACITY', 1))


class SCAMemoryHandler(MemoryHandler):
    def __init__(self, capacity: int, log_group_name: str):
        self.log_group_name = log_group_name
        logging.Handler.__init__(self)
        super().__init__(capacity=capacity)

    def upload_to_kinesis(self, byte_stream: BytesIO) -> None:
        kinesis_client = utils.kinesis_client()
        kinesis_client.put_record(Data=byte_stream.getvalue(),
                                  StreamName=KINESIS_SCA_LOG_STREAM,
                                  PartitionKey=self.log_group_name)

    @staticmethod
    def _serialize(thing):
        return json.dumps(thing, sort_keys=True, indent=4, default=str)

    def _prep_serialize(self, thing):
        try:
            self._serialize(thing)
            return thing
        except Exception as the_error:
            # print(f'Encountered {the_error} serializing {thing}. ' +
            #       'Will try to cast it to a str.')
            pass
        try:
            return str(thing)
        except Exception as the_error:
            # print(f'Encountered {the_error} stringifying {thing}. Skipping.')
            return ''

    def flush(self):
        self.acquire()
        try:
            if len(self.buffer) != 0:
                formatted_records = list()
                byte_stream = io.BytesIO()
                with gzip.GzipFile(mode='wb', fileobj=byte_stream) as gz:
                    for record in self.buffer:
                        formatted = self.format(record)
                        safe_to_serialize = self._prep_serialize(formatted)
                        formatted_records.append(safe_to_serialize)
                    serialized_records = self._serialize(formatted_records)
                    gz.write(serialized_records.encode("utf-8"))
                self.upload_to_kinesis(byte_stream)
                byte_stream.close()
                self.buffer = []
        finally:
            self.release()
