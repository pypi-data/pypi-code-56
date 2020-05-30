# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from python2sky.proto.common import common_pb2 as common_dot_common__pb2
from python2sky.proto.language_agent_v2 import JVMMetric_pb2 as language__agent__v2_dot_JVMMetric__pb2


class JVMMetricReportServiceStub(object):
    """Missing associated documentation comment in .proto file"""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.collect = channel.unary_unary(
                '/JVMMetricReportService/collect',
                request_serializer=language__agent__v2_dot_JVMMetric__pb2.JVMMetricCollection.SerializeToString,
                response_deserializer=common_dot_common__pb2.Commands.FromString,
                )


class JVMMetricReportServiceServicer(object):
    """Missing associated documentation comment in .proto file"""

    def collect(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_JVMMetricReportServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'collect': grpc.unary_unary_rpc_method_handler(
                    servicer.collect,
                    request_deserializer=language__agent__v2_dot_JVMMetric__pb2.JVMMetricCollection.FromString,
                    response_serializer=common_dot_common__pb2.Commands.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'JVMMetricReportService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class JVMMetricReportService(object):
    """Missing associated documentation comment in .proto file"""

    @staticmethod
    def collect(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/JVMMetricReportService/collect',
            language__agent__v2_dot_JVMMetric__pb2.JVMMetricCollection.SerializeToString,
            common_dot_common__pb2.Commands.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)
