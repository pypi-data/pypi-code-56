# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from . import mission_raw_pb2 as mission__raw__pb2


class MissionRawServiceStub(object):
    """Enable raw missions as exposed by MAVLink.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.UploadMission = channel.unary_unary(
                '/mavsdk.rpc.mission_raw.MissionRawService/UploadMission',
                request_serializer=mission__raw__pb2.UploadMissionRequest.SerializeToString,
                response_deserializer=mission__raw__pb2.UploadMissionResponse.FromString,
                )
        self.CancelMissionUpload = channel.unary_unary(
                '/mavsdk.rpc.mission_raw.MissionRawService/CancelMissionUpload',
                request_serializer=mission__raw__pb2.CancelMissionUploadRequest.SerializeToString,
                response_deserializer=mission__raw__pb2.CancelMissionUploadResponse.FromString,
                )
        self.DownloadMission = channel.unary_unary(
                '/mavsdk.rpc.mission_raw.MissionRawService/DownloadMission',
                request_serializer=mission__raw__pb2.DownloadMissionRequest.SerializeToString,
                response_deserializer=mission__raw__pb2.DownloadMissionResponse.FromString,
                )
        self.CancelMissionDownload = channel.unary_unary(
                '/mavsdk.rpc.mission_raw.MissionRawService/CancelMissionDownload',
                request_serializer=mission__raw__pb2.CancelMissionDownloadRequest.SerializeToString,
                response_deserializer=mission__raw__pb2.CancelMissionDownloadResponse.FromString,
                )
        self.StartMission = channel.unary_unary(
                '/mavsdk.rpc.mission_raw.MissionRawService/StartMission',
                request_serializer=mission__raw__pb2.StartMissionRequest.SerializeToString,
                response_deserializer=mission__raw__pb2.StartMissionResponse.FromString,
                )
        self.PauseMission = channel.unary_unary(
                '/mavsdk.rpc.mission_raw.MissionRawService/PauseMission',
                request_serializer=mission__raw__pb2.PauseMissionRequest.SerializeToString,
                response_deserializer=mission__raw__pb2.PauseMissionResponse.FromString,
                )
        self.ClearMission = channel.unary_unary(
                '/mavsdk.rpc.mission_raw.MissionRawService/ClearMission',
                request_serializer=mission__raw__pb2.ClearMissionRequest.SerializeToString,
                response_deserializer=mission__raw__pb2.ClearMissionResponse.FromString,
                )
        self.SetCurrentMissionItem = channel.unary_unary(
                '/mavsdk.rpc.mission_raw.MissionRawService/SetCurrentMissionItem',
                request_serializer=mission__raw__pb2.SetCurrentMissionItemRequest.SerializeToString,
                response_deserializer=mission__raw__pb2.SetCurrentMissionItemResponse.FromString,
                )
        self.SubscribeMissionProgress = channel.unary_stream(
                '/mavsdk.rpc.mission_raw.MissionRawService/SubscribeMissionProgress',
                request_serializer=mission__raw__pb2.SubscribeMissionProgressRequest.SerializeToString,
                response_deserializer=mission__raw__pb2.MissionProgressResponse.FromString,
                )
        self.SubscribeMissionChanged = channel.unary_stream(
                '/mavsdk.rpc.mission_raw.MissionRawService/SubscribeMissionChanged',
                request_serializer=mission__raw__pb2.SubscribeMissionChangedRequest.SerializeToString,
                response_deserializer=mission__raw__pb2.MissionChangedResponse.FromString,
                )


class MissionRawServiceServicer(object):
    """Enable raw missions as exposed by MAVLink.
    """

    def UploadMission(self, request, context):
        """
        Upload a list of raw mission items to the system.

        The raw mission items are uploaded to a drone. Once uploaded the mission
        can be started and executed even if the connection is lost.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CancelMissionUpload(self, request, context):
        """
        Cancel an ongoing mission upload.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DownloadMission(self, request, context):
        """
        Download a list of raw mission items from the system (asynchronous).
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CancelMissionDownload(self, request, context):
        """
        Cancel an ongoing mission download.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def StartMission(self, request, context):
        """
        Start the mission.

        A mission must be uploaded to the vehicle before this can be called.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def PauseMission(self, request, context):
        """
        Pause the mission.

        Pausing the mission puts the vehicle into
        [HOLD mode](https://docs.px4.io/en/flight_modes/hold.html).
        A multicopter should just hover at the spot while a fixedwing vehicle should loiter
        around the location where it paused.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ClearMission(self, request, context):
        """
        Clear the mission saved on the vehicle.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SetCurrentMissionItem(self, request, context):
        """
        Sets the raw mission item index to go to.

        By setting the current index to 0, the mission is restarted from the beginning. If it is set
        to a specific index of a raw mission item, the mission will be set to this item.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SubscribeMissionProgress(self, request, context):
        """
        Subscribe to mission progress updates.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SubscribeMissionChanged(self, request, context):
        """*
        Subscribes to mission changed.

        This notification can be used to be informed if a ground station has
        been uploaded or changed by a ground station or companion computer.

        @param callback Callback to notify about change.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_MissionRawServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'UploadMission': grpc.unary_unary_rpc_method_handler(
                    servicer.UploadMission,
                    request_deserializer=mission__raw__pb2.UploadMissionRequest.FromString,
                    response_serializer=mission__raw__pb2.UploadMissionResponse.SerializeToString,
            ),
            'CancelMissionUpload': grpc.unary_unary_rpc_method_handler(
                    servicer.CancelMissionUpload,
                    request_deserializer=mission__raw__pb2.CancelMissionUploadRequest.FromString,
                    response_serializer=mission__raw__pb2.CancelMissionUploadResponse.SerializeToString,
            ),
            'DownloadMission': grpc.unary_unary_rpc_method_handler(
                    servicer.DownloadMission,
                    request_deserializer=mission__raw__pb2.DownloadMissionRequest.FromString,
                    response_serializer=mission__raw__pb2.DownloadMissionResponse.SerializeToString,
            ),
            'CancelMissionDownload': grpc.unary_unary_rpc_method_handler(
                    servicer.CancelMissionDownload,
                    request_deserializer=mission__raw__pb2.CancelMissionDownloadRequest.FromString,
                    response_serializer=mission__raw__pb2.CancelMissionDownloadResponse.SerializeToString,
            ),
            'StartMission': grpc.unary_unary_rpc_method_handler(
                    servicer.StartMission,
                    request_deserializer=mission__raw__pb2.StartMissionRequest.FromString,
                    response_serializer=mission__raw__pb2.StartMissionResponse.SerializeToString,
            ),
            'PauseMission': grpc.unary_unary_rpc_method_handler(
                    servicer.PauseMission,
                    request_deserializer=mission__raw__pb2.PauseMissionRequest.FromString,
                    response_serializer=mission__raw__pb2.PauseMissionResponse.SerializeToString,
            ),
            'ClearMission': grpc.unary_unary_rpc_method_handler(
                    servicer.ClearMission,
                    request_deserializer=mission__raw__pb2.ClearMissionRequest.FromString,
                    response_serializer=mission__raw__pb2.ClearMissionResponse.SerializeToString,
            ),
            'SetCurrentMissionItem': grpc.unary_unary_rpc_method_handler(
                    servicer.SetCurrentMissionItem,
                    request_deserializer=mission__raw__pb2.SetCurrentMissionItemRequest.FromString,
                    response_serializer=mission__raw__pb2.SetCurrentMissionItemResponse.SerializeToString,
            ),
            'SubscribeMissionProgress': grpc.unary_stream_rpc_method_handler(
                    servicer.SubscribeMissionProgress,
                    request_deserializer=mission__raw__pb2.SubscribeMissionProgressRequest.FromString,
                    response_serializer=mission__raw__pb2.MissionProgressResponse.SerializeToString,
            ),
            'SubscribeMissionChanged': grpc.unary_stream_rpc_method_handler(
                    servicer.SubscribeMissionChanged,
                    request_deserializer=mission__raw__pb2.SubscribeMissionChangedRequest.FromString,
                    response_serializer=mission__raw__pb2.MissionChangedResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'mavsdk.rpc.mission_raw.MissionRawService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class MissionRawService(object):
    """Enable raw missions as exposed by MAVLink.
    """

    @staticmethod
    def UploadMission(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mavsdk.rpc.mission_raw.MissionRawService/UploadMission',
            mission__raw__pb2.UploadMissionRequest.SerializeToString,
            mission__raw__pb2.UploadMissionResponse.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CancelMissionUpload(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mavsdk.rpc.mission_raw.MissionRawService/CancelMissionUpload',
            mission__raw__pb2.CancelMissionUploadRequest.SerializeToString,
            mission__raw__pb2.CancelMissionUploadResponse.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DownloadMission(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mavsdk.rpc.mission_raw.MissionRawService/DownloadMission',
            mission__raw__pb2.DownloadMissionRequest.SerializeToString,
            mission__raw__pb2.DownloadMissionResponse.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CancelMissionDownload(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mavsdk.rpc.mission_raw.MissionRawService/CancelMissionDownload',
            mission__raw__pb2.CancelMissionDownloadRequest.SerializeToString,
            mission__raw__pb2.CancelMissionDownloadResponse.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def StartMission(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mavsdk.rpc.mission_raw.MissionRawService/StartMission',
            mission__raw__pb2.StartMissionRequest.SerializeToString,
            mission__raw__pb2.StartMissionResponse.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def PauseMission(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mavsdk.rpc.mission_raw.MissionRawService/PauseMission',
            mission__raw__pb2.PauseMissionRequest.SerializeToString,
            mission__raw__pb2.PauseMissionResponse.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ClearMission(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mavsdk.rpc.mission_raw.MissionRawService/ClearMission',
            mission__raw__pb2.ClearMissionRequest.SerializeToString,
            mission__raw__pb2.ClearMissionResponse.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SetCurrentMissionItem(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mavsdk.rpc.mission_raw.MissionRawService/SetCurrentMissionItem',
            mission__raw__pb2.SetCurrentMissionItemRequest.SerializeToString,
            mission__raw__pb2.SetCurrentMissionItemResponse.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SubscribeMissionProgress(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/mavsdk.rpc.mission_raw.MissionRawService/SubscribeMissionProgress',
            mission__raw__pb2.SubscribeMissionProgressRequest.SerializeToString,
            mission__raw__pb2.MissionProgressResponse.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SubscribeMissionChanged(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/mavsdk.rpc.mission_raw.MissionRawService/SubscribeMissionChanged',
            mission__raw__pb2.SubscribeMissionChangedRequest.SerializeToString,
            mission__raw__pb2.MissionChangedResponse.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)
