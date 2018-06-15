import sys
import os
import unittest
import json
import requests

from unittest import mock
from SpiffWorkflow import Workflow, Task
from SpiffWorkflow.specs import WorkflowSpec

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from pf_spiff_workflow.specs.Rest import GetRequest
from pf_spiff_workflow.serializers.serializer import PortalSerializer


GOOD_GET_FLOW_FILEPATH = 'resources/test_flow_get_02.json'
BAD_GET_FLOW_FILEPATH = 'resources/test_flow_get_01.json'
GOOD_POST_FLOW_FILEPATH = 'resources/test_flow_post_02.json'
BAD_POST_FLOW_FILEPATH = 'resources/test_flow_post_01.json'
GOOD_PUT_FLOW_FILEPATH = 'resources/test_flow_put_02.json'
BAD_PUT_FLOW_FILEPATH = 'resources/test_flow_put_01.json'
GOOD_DELETE_FLOW_FILEPATH = 'resources/test_flow_delete_02.json'
BAD_DELETE_FLOW_FILEPATH = 'resources/test_flow_delete_01.json'


def load_json_string(directory):

    current_path = os.path.realpath('__file__')
    current_directory = os.path.dirname(current_path)
    file_path = os.path.join(current_directory, directory)
    
    json_string = None
    with open(file_path) as file:
        json_data = file.read()
        json_content = json.loads(json_data)
        json_string = json.dumps(json_content)

    if json_string is None:
        raise Exception()
    
    return json_string


# This method will be used by the mock to replace requests methods
def mocked_requests(*args, **kwargs):
    
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data
    filter_params = {'params': {'filter_1': 'test_1'}}
    if args[0] == 'http://someurl.com' and kwargs == filter_params:
        return MockResponse({"key1": "value1"}, 200)

    return MockResponse(None, 404)


class RestWorkflowTestCase(unittest.TestCase):

    def load_workflow(self, test_file_path):
        json_string = load_json_string(test_file_path)

        workflow_spec = WorkflowSpec.deserialize(self.serializer, 
                                                 json_string)
        self.workflow = Workflow(workflow_spec)

    def setUp(self):
        self.serializer = PortalSerializer()

    def tearDown(self):
        self.serializer = None
        self.workflow = None


class TestGetRequest(RestWorkflowTestCase):

    def test_can_deserialize_task(self):
        
        try:
            self.load_workflow(GOOD_GET_FLOW_FILEPATH)
        except Exception as e:
            self.assertTrue(False)
        self.assertIsNotNone(self.workflow)

    @mock.patch('requests.get', side_effect = mocked_requests)
    def test_can_run_workflow_with_task(self, mock_get):
        
        self.load_workflow(GOOD_GET_FLOW_FILEPATH)
        
        try:
            self.workflow.complete_all(halt_on_manual=False)
        except Exception as e:
            self.assertTrue(False)
        
        self.assertTrue(True)

    @mock.patch('requests.get', side_effect = mocked_requests)
    def test_fails_to_incorrect_url(self, mock_get):
        
        self.load_workflow(BAD_GET_FLOW_FILEPATH)
        
        self.workflow.complete_all(halt_on_manual=False)
        tasks = self.workflow.get_tasks_from_spec_name('task_under_test')
        task = tasks[0]

        result = task.get_data('response_code')    
        self.assertEqual(result, 404)

    @mock.patch('requests.get', side_effect = mocked_requests)
    def test_fails_without_url_parameters(self, mock_get):
        
        self.load_workflow(BAD_GET_FLOW_FILEPATH)
        
        self.workflow.complete_all(halt_on_manual=False)
        tasks = self.workflow.get_tasks_from_spec_name('task_under_test')
        task = tasks[0]

        result = task.get_data('response_code')    
        self.assertEqual(result, 404)

    @mock.patch('requests.get', side_effect = mocked_requests)
    def test_sets_did_make_request(self, mock_get):
        
        self.load_workflow(GOOD_GET_FLOW_FILEPATH)
        
        self.workflow.complete_all(halt_on_manual=False)
        tasks = self.workflow.get_tasks_from_spec_name('task_under_test')
        task = tasks[0]

        result = task.get_data('did_make_request')
        self.assertTrue(result)

    @mock.patch('requests.get', side_effect = mocked_requests)
    def test_sets_response_code(self, mock_get):
        
        self.load_workflow(GOOD_GET_FLOW_FILEPATH)
        
        self.workflow.complete_all(halt_on_manual=False)
        tasks = self.workflow.get_tasks_from_spec_name('task_under_test')
        task = tasks[0]

        result = task.get_data('response_code')
        self.assertIsNotNone(result)   
        self.assertEqual(result, 200)

    @mock.patch('requests.get', side_effect = mocked_requests)
    def test_sets_response_body(self, mock_get):
        
        self.load_workflow(GOOD_GET_FLOW_FILEPATH)
        
        self.workflow.complete_all(halt_on_manual=False)
        tasks = self.workflow.get_tasks_from_spec_name('task_under_test')
        task = tasks[0]

        result = task.get_data('response_body')    
        self.assertIsNotNone(result)
        self.assertEqual(result, {"key1": "value1"})


class PostRequestTest(RestWorkflowTestCase):

    def test_can_deserialize_task(self):
        try:
            self.load_workflow(GOOD_POST_FLOW_FILEPATH)
        except Exception as e:
            self.assertTrue(False)
        self.assertIsNotNone(self.workflow)

    @mock.patch('requests.post', side_effect = mocked_requests)
    def test_can_run_workflow_with_task(self, mock_post):
        self.load_workflow(GOOD_POST_FLOW_FILEPATH)
        
        try:
            self.workflow.complete_all(halt_on_manual=False)
        except Exception as e:
            self.assertTrue(False)
        
        self.assertTrue(True)

    @mock.patch('requests.post', side_effect = mocked_requests)
    def test_fails_to_incorrect_url(self, mock_post):
        self.load_workflow(BAD_POST_FLOW_FILEPATH)
        
        self.workflow.complete_all(halt_on_manual=False)
        tasks = self.workflow.get_tasks_from_spec_name('task_under_test')
        task = tasks[0]

        result = task.get_data('response_code')    
        self.assertEqual(result, 404)

    @mock.patch('requests.post', side_effect = mocked_requests)
    def test_fails_without_body_parameters(self, mock_post):

        self.load_workflow(BAD_POST_FLOW_FILEPATH)
        
        self.workflow.complete_all(halt_on_manual=False)
        tasks = self.workflow.get_tasks_from_spec_name('task_under_test')
        task = tasks[0]

        result = task.get_data('response_code')    
        self.assertEqual(result, 404)


    @mock.patch('requests.post', side_effect = mocked_requests)
    def test_sets_did_make_request(self, mock_post):

        self.load_workflow(GOOD_POST_FLOW_FILEPATH)
        
        self.workflow.complete_all(halt_on_manual=False)
        tasks = self.workflow.get_tasks_from_spec_name('task_under_test')
        task = tasks[0]

        result = task.get_data('did_make_request')
        self.assertTrue(result)

    @mock.patch('requests.post', side_effect = mocked_requests)
    def test_sets_response_code(self, mock_post):

        self.load_workflow(GOOD_POST_FLOW_FILEPATH)
        
        self.workflow.complete_all(halt_on_manual=False)
        tasks = self.workflow.get_tasks_from_spec_name('task_under_test')
        task = tasks[0]

        result = task.get_data('response_code')
        self.assertIsNotNone(result)   
        self.assertEqual(result, 200)

    @mock.patch('requests.post', side_effect = mocked_requests)
    def test_sets_response_body(self, mock_post):

        self.load_workflow(GOOD_POST_FLOW_FILEPATH)
        
        self.workflow.complete_all(halt_on_manual=False)
        tasks = self.workflow.get_tasks_from_spec_name('task_under_test')
        task = tasks[0]

        result = task.get_data('response_body')    
        self.assertIsNotNone(result)
        self.assertEqual(result, {"key1": "value1"})


class PutRequestTest(RestWorkflowTestCase):

    def test_can_deserialize_task(self):
        try:
            self.load_workflow(GOOD_PUT_FLOW_FILEPATH)
        except Exception as e:
            self.assertTrue(False)
        self.assertIsNotNone(self.workflow)

    @mock.patch('requests.put', side_effect = mocked_requests)
    def test_can_run_workflow_with_task(self, mock_put):
        self.load_workflow(GOOD_PUT_FLOW_FILEPATH)
        
        try:
            self.workflow.complete_all(halt_on_manual=False)
        except Exception as e:
            self.assertTrue(False)
        
        self.assertTrue(True)

    @mock.patch('requests.put', side_effect = mocked_requests)
    def test_fails_to_incorrect_url(self, mock_put):
        self.load_workflow(BAD_PUT_FLOW_FILEPATH)
        
        self.workflow.complete_all(halt_on_manual=False)
        tasks = self.workflow.get_tasks_from_spec_name('task_under_test')
        task = tasks[0]

        result = task.get_data('response_code')    
        self.assertEqual(result, 404)

    @mock.patch('requests.put', side_effect = mocked_requests)
    def test_fails_without_body_parameters(self, mock_put):

        self.load_workflow(BAD_PUT_FLOW_FILEPATH)
        
        self.workflow.complete_all(halt_on_manual=False)
        tasks = self.workflow.get_tasks_from_spec_name('task_under_test')
        task = tasks[0]

        result = task.get_data('response_code')    
        self.assertEqual(result, 404)

    @mock.patch('requests.put', side_effect = mocked_requests)
    def test_sets_did_make_request(self, mock_put):

        self.load_workflow(GOOD_PUT_FLOW_FILEPATH)
        
        self.workflow.complete_all(halt_on_manual=False)
        tasks = self.workflow.get_tasks_from_spec_name('task_under_test')
        task = tasks[0]

        result = task.get_data('did_make_request')
        self.assertTrue(result)

    @mock.patch('requests.put', side_effect = mocked_requests)
    def test_sets_response_code(self, mock_put):

        self.load_workflow(GOOD_PUT_FLOW_FILEPATH)
        
        self.workflow.complete_all(halt_on_manual=False)
        tasks = self.workflow.get_tasks_from_spec_name('task_under_test')
        task = tasks[0]

        result = task.get_data('response_code')
        self.assertIsNotNone(result)   
        self.assertEqual(result, 200)

    @mock.patch('requests.put', side_effect = mocked_requests)
    def test_sets_response_body(self, mock_put):

        self.load_workflow(GOOD_PUT_FLOW_FILEPATH)
        
        self.workflow.complete_all(halt_on_manual=False)
        tasks = self.workflow.get_tasks_from_spec_name('task_under_test')
        task = tasks[0]

        result = task.get_data('response_body')    
        self.assertIsNotNone(result)
        self.assertEqual(result, {"key1": "value1"})


class DeleteRequestTest(RestWorkflowTestCase):

    def test_can_deserialize_task(self):
        try:
            self.load_workflow(GOOD_DELETE_FLOW_FILEPATH)
        except Exception as e:
            self.assertTrue(False)
        self.assertIsNotNone(self.workflow)

    @mock.patch('requests.delete', side_effect = mocked_requests)
    def test_can_run_workflow_with_task(self, mock_delete):
        self.load_workflow(GOOD_DELETE_FLOW_FILEPATH)
        
        try:
            self.workflow.complete_all(halt_on_manual=False)
        except Exception as e:
            self.assertTrue(False)
        
        self.assertTrue(True)

    @mock.patch('requests.delete', side_effect = mocked_requests)
    def test_fails_to_incorrect_url(self, mock_delete):
        self.load_workflow(BAD_DELETE_FLOW_FILEPATH)
        
        self.workflow.complete_all(halt_on_manual=False)
        tasks = self.workflow.get_tasks_from_spec_name('task_under_test')
        task = tasks[0]

        result = task.get_data('response_code')    
        self.assertEqual(result, 404)

    @mock.patch('requests.delete', side_effect = mocked_requests)
    def test_sets_did_make_request(self, mock_delete):

        self.load_workflow(GOOD_DELETE_FLOW_FILEPATH)
        
        self.workflow.complete_all(halt_on_manual=False)
        tasks = self.workflow.get_tasks_from_spec_name('task_under_test')
        task = tasks[0]

        result = task.get_data('did_make_request')
        self.assertTrue(result)

    @mock.patch('requests.delete', side_effect = mocked_requests)
    def test_sets_response_code(self, mock_delete):

        self.load_workflow(GOOD_DELETE_FLOW_FILEPATH)
        
        self.workflow.complete_all(halt_on_manual=False)
        tasks = self.workflow.get_tasks_from_spec_name('task_under_test')
        task = tasks[0]

        result = task.get_data('response_code')
        self.assertIsNotNone(result)   
        self.assertEqual(result, 200)

    @mock.patch('requests.delete', side_effect = mocked_requests)
    def test_sets_response_body(self, mock_delete):

        self.load_workflow(GOOD_DELETE_FLOW_FILEPATH)
        
        self.workflow.complete_all(halt_on_manual=False)
        tasks = self.workflow.get_tasks_from_spec_name('task_under_test')
        task = tasks[0]

        result = task.get_data('response_body')    
        self.assertIsNotNone(result)
        self.assertEqual(result, {"key1": "value1"})


def suite():
    suite = unittest.TestSuite()
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
