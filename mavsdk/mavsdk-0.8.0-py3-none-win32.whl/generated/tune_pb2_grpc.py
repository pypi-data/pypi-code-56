# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from . import tune_pb2 as tune__pb2


class TuneServiceStub(object):
    """Enable creating and sending a tune to be played on the system.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.PlayTune = channel.unary_unary(
                '/mavsdk.rpc.tune.TuneService/PlayTune',
                request_serializer=tune__pb2.PlayTuneRequest.SerializeToString,
                response_deserializer=tune__pb2.PlayTuneResponse.FromString,
                )


class TuneServiceServicer(object):
    """Enable creating and sending a tune to be played on the system.
    """

    def PlayTune(self, request, context):
        """Send a tune to be played by the system.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_TuneServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'PlayTune': grpc.unary_unary_rpc_method_handler(
                    servicer.PlayTune,
                    request_deserializer=tune__pb2.PlayTuneRequest.FromString,
                    response_serializer=tune__pb2.PlayTuneResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'mavsdk.rpc.tune.TuneService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class TuneService(object):
    """Enable creating and sending a tune to be played on the system.
    """

    @staticmethod
    def PlayTune(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mavsdk.rpc.tune.TuneService/PlayTune',
            tune__pb2.PlayTuneRequest.SerializeToString,
            tune__pb2.PlayTuneResponse.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)
