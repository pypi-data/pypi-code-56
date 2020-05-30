# Generated by the Protocol Buffers compiler. DO NOT EDIT!
# source: grpclib/reflection/v1/reflection.proto
# plugin: grpclib.plugin.main
import abc
import typing

import grpclib.const
import grpclib.client
if typing.TYPE_CHECKING:
    import grpclib.server

import grpclib.reflection.v1.reflection_pb2


class ServerReflectionBase(abc.ABC):

    @abc.abstractmethod
    async def ServerReflectionInfo(self, stream: 'grpclib.server.Stream[grpclib.reflection.v1.reflection_pb2.ServerReflectionRequest, grpclib.reflection.v1.reflection_pb2.ServerReflectionResponse]') -> None:
        pass

    def __mapping__(self) -> typing.Dict[str, grpclib.const.Handler]:
        return {
            '/grpc.reflection.v1.ServerReflection/ServerReflectionInfo': grpclib.const.Handler(
                self.ServerReflectionInfo,
                grpclib.const.Cardinality.STREAM_STREAM,
                grpclib.reflection.v1.reflection_pb2.ServerReflectionRequest,
                grpclib.reflection.v1.reflection_pb2.ServerReflectionResponse,
            ),
        }


class ServerReflectionStub:

    def __init__(self, channel: grpclib.client.Channel) -> None:
        self.ServerReflectionInfo = grpclib.client.StreamStreamMethod(
            channel,
            '/grpc.reflection.v1.ServerReflection/ServerReflectionInfo',
            grpclib.reflection.v1.reflection_pb2.ServerReflectionRequest,
            grpclib.reflection.v1.reflection_pb2.ServerReflectionResponse,
        )
