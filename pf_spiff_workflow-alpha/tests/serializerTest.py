from __future__ import print_function
from SpiffWorkflow.serializer.json import JSONSerializer
from .specs.Rest import *


class PortalSerializer(JSONSerializer):
    """
    EN:
    A Customization of the SpiffWorkflow JSONSerializer that will be 
    able to SERIALIZE and DESERIALIZE the Portal Finance TASK SPECS
    
    ES:
    Una personalización del SpiffWorkflow JSONSerializer que será capaz 
    de serializar y deserializar las especificaciones de la tarea de 
    finanzas del portal
    """

    REQUEST_URL = 'url'
    REQUEST_AUTH = 'auth'
    REQUEST_BODY = 'body'
    REQUEST_HEADER = 'header'

    def __parse_task_state(self, rest_request_spec, s_state):
        """
        EN:
        Parses the REST REQUEST VARIABLES from the s_state variables and 
        constructs the REST REQUEST TASK

        ARGUMENTS:
            rest_request_spec - The REST REQUEST TASK SPEC that is being 
            DESERIALIZED
            s_state - This variables contains a dictionary of the variables that
            are includedin the Workflow Specification.

        ES:
        Analiza las variables de solicitud REST de las variables de 
        estado s y construye la tarea de solicitud REST

        PARAMETROS:
        
        """

        rest_request_spec.url = s_state[PortalSerializer.REQUEST_URL]
        rest_request_spec.body = s_state[PortalSerializer.REQUEST_BODY]
        rest_request_spec.header = s_state[PortalSerializer.REQUEST_HEADER]
        
        return rest_request_spec

    def serialize_get_request(self, task_spec):
        return self.serialize_task_spec(task_spec)

    def deserialize_get_request(self, wf_spec, s_state):
        spec = GetRequest(wf_spec, s_state['name'])
        self.deserialize_task_spec(wf_spec, s_state, spec=spec)
        spec = self.__parse_task_state(spec, s_state)
        return spec

    def serialize_post_request(self, task_spec):
        return self.serialize_task_spec(task_spec)

    def deserialize_post_request(self, wf_spec, s_state):
        spec = PostRequest(wf_spec, s_state['name'])
        self.deserialize_task_spec(wf_spec, s_state, spec=spec)
        spec = self.__parse_task_state(spec, s_state)
        return spec

    def serialize_put_request(self, task_spec):
        return self.serialize_task_spec(task_spec)

    def deserialize_put_request(self, wf_spec, s_state):
        spec = PutRequest(wf_spec, s_state['name'])
        self.deserialize_task_spec(wf_spec, s_state, spec=spec)
        spec = self.__parse_task_state(spec, s_state)
        return spec

    def serialize_delete_request(self, task_spec):
        return self.serialize_task_spec(task_spec)

    def deserialize_delete_request(self, wf_spec, s_state):
        spec = DeleteRequest(wf_spec, s_state['name'])
        self.deserialize_task_spec(wf_spec, s_state, spec=spec)
        spec = self.__parse_task_state(spec, s_state)
        return spec
