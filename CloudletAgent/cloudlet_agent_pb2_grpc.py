# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from CloudletAgent import cloudlet_agent_pb2 as CloudletAgent_dot_cloudlet__agent__pb2


class CloudletsAPIStub(object):
    """Методы Cloudlets Service, которыми пользуется Cloudlet Agent
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Add = channel.unary_unary(
                '/CloudletsAPI/Add',
                request_serializer=CloudletAgent_dot_cloudlet__agent__pb2.Cloudlet.SerializeToString,
                response_deserializer=CloudletAgent_dot_cloudlet__agent__pb2.ResponseWithCloudlet.FromString,
                )


class CloudletsAPIServicer(object):
    """Методы Cloudlets Service, которыми пользуется Cloudlet Agent
    """

    def Add(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_CloudletsAPIServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Add': grpc.unary_unary_rpc_method_handler(
                    servicer.Add,
                    request_deserializer=CloudletAgent_dot_cloudlet__agent__pb2.Cloudlet.FromString,
                    response_serializer=CloudletAgent_dot_cloudlet__agent__pb2.ResponseWithCloudlet.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'CloudletsAPI', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class CloudletsAPI(object):
    """Методы Cloudlets Service, которыми пользуется Cloudlet Agent
    """

    @staticmethod
    def Add(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/CloudletsAPI/Add',
            CloudletAgent_dot_cloudlet__agent__pb2.Cloudlet.SerializeToString,
            CloudletAgent_dot_cloudlet__agent__pb2.ResponseWithCloudlet.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)