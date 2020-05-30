# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from . import gimbal_pb2 as gimbal__pb2


class GimbalServiceStub(object):
    """Provide control over a gimbal.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.SetPitchAndYaw = channel.unary_unary(
                '/mavsdk.rpc.gimbal.GimbalService/SetPitchAndYaw',
                request_serializer=gimbal__pb2.SetPitchAndYawRequest.SerializeToString,
                response_deserializer=gimbal__pb2.SetPitchAndYawResponse.FromString,
                )
        self.SetMode = channel.unary_unary(
                '/mavsdk.rpc.gimbal.GimbalService/SetMode',
                request_serializer=gimbal__pb2.SetModeRequest.SerializeToString,
                response_deserializer=gimbal__pb2.SetModeResponse.FromString,
                )
        self.SetRoiLocation = channel.unary_unary(
                '/mavsdk.rpc.gimbal.GimbalService/SetRoiLocation',
                request_serializer=gimbal__pb2.SetRoiLocationRequest.SerializeToString,
                response_deserializer=gimbal__pb2.SetRoiLocationResponse.FromString,
                )


class GimbalServiceServicer(object):
    """Provide control over a gimbal.
    """

    def SetPitchAndYaw(self, request, context):
        """

        Set gimbal pitch and yaw angles.

        This sets the desired pitch and yaw angles of a gimbal.
        Will return when the command is accepted, however, it might
        take the gimbal longer to actually be set to the new angles.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SetMode(self, request, context):
        """
        Set gimbal mode.

        This sets the desired yaw mode of a gimbal.
        Will return when the command is accepted. However, it might
        take the gimbal longer to actually be set to the new angles.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SetRoiLocation(self, request, context):
        """
        Set gimbal region of interest (ROI).

        This sets a region of interest that the gimbal will point to.
        The gimbal will continue to point to the specified region until it
        receives a new command.
        The function will return when the command is accepted, however, it might
        take the gimbal longer to actually rotate to the ROI.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_GimbalServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'SetPitchAndYaw': grpc.unary_unary_rpc_method_handler(
                    servicer.SetPitchAndYaw,
                    request_deserializer=gimbal__pb2.SetPitchAndYawRequest.FromString,
                    response_serializer=gimbal__pb2.SetPitchAndYawResponse.SerializeToString,
            ),
            'SetMode': grpc.unary_unary_rpc_method_handler(
                    servicer.SetMode,
                    request_deserializer=gimbal__pb2.SetModeRequest.FromString,
                    response_serializer=gimbal__pb2.SetModeResponse.SerializeToString,
            ),
            'SetRoiLocation': grpc.unary_unary_rpc_method_handler(
                    servicer.SetRoiLocation,
                    request_deserializer=gimbal__pb2.SetRoiLocationRequest.FromString,
                    response_serializer=gimbal__pb2.SetRoiLocationResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'mavsdk.rpc.gimbal.GimbalService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class GimbalService(object):
    """Provide control over a gimbal.
    """

    @staticmethod
    def SetPitchAndYaw(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mavsdk.rpc.gimbal.GimbalService/SetPitchAndYaw',
            gimbal__pb2.SetPitchAndYawRequest.SerializeToString,
            gimbal__pb2.SetPitchAndYawResponse.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SetMode(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mavsdk.rpc.gimbal.GimbalService/SetMode',
            gimbal__pb2.SetModeRequest.SerializeToString,
            gimbal__pb2.SetModeResponse.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SetRoiLocation(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mavsdk.rpc.gimbal.GimbalService/SetRoiLocation',
            gimbal__pb2.SetRoiLocationRequest.SerializeToString,
            gimbal__pb2.SetRoiLocationResponse.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)
