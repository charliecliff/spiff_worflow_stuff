from __future__ import print_function
from SpiffWorkflow.specs import Simple
import requests
import json
        

class GetRequest(Simple):
    """
    Feilds:
        url
        body
        header
        did_make_request
        response_code
        response_body
    """

    def _on_complete_hook(self, my_task):

        try:
            http_request = requests.get(self.url, params=self.filters)
        except Exception as e:
            self.did_make_request = False
            return

        my_task.set_data(did_make_request=True)
        my_task.set_data(response_code=http_request.status_code )
        
        json_response = http_request.json()
        my_task.set_data(response_body=json_response)

    def serialize(self, serializer):
        return serializer.serialize_get_request(self)

    @classmethod
    def deserialize(self, serializer, wf_spec, s_state):
        return serializer.deserialize_get_request(wf_spec, s_state)


class PostRequest(Simple):

    def _on_complete_hook(self, my_task):
        
        try:
            http_request = requests.post(self.url, params=self.filters)
        except Exception as e:
            self.did_make_request = False
            return

        my_task.set_data(did_make_request=True)
        my_task.set_data(response_code=http_request.status_code )
        
        json_response = http_request.json()
        my_task.set_data(response_body=json_response)

    def serialize(self, serializer):
        return serializer.serialize_post_request(self)

    @classmethod
    def deserialize(self, serializer, wf_spec, s_state):
        return serializer.deserialize_post_request(wf_spec, s_state)


class PutRequest(Simple):

    def _on_complete_hook(self, my_task):

        try:
            http_request = requests.put(self.url, params=self.filters)
        except Exception as e:
            self.did_make_request = False
            return

        my_task.set_data(did_make_request=True)
        my_task.set_data(response_code=http_request.status_code )

        json_response = http_request.json()
        my_task.set_data(response_body=json_response)

    def serialize(self, serializer):
        return serializer.serialize_put_request(self)

    @classmethod
    def deserialize(self, serializer, wf_spec, s_state):
        return serializer.deserialize_put_request(wf_spec, s_state)


class DeleteRequest(Simple):

    def _on_complete_hook(self, my_task):

        try:
            http_request = requests.delete(self.url, params=self.filters)
        except Exception as e:
            self.did_make_request = False
            return

        my_task.set_data(did_make_request=True)
        my_task.set_data(response_code=http_request.status_code )

        json_response = http_request.json()
        my_task.set_data(response_body=json_response)
        
    def serialize(self, serializer):
        return serializer.serialize_delete_request(self)

    @classmethod
    def deserialize(self, serializer, wf_spec, s_state):
        return serializer.deserialize_delete_request(wf_spec, s_state)
