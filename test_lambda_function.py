import json
import unittest
from unittest.mock import MagicMock, patch

from botocore.exceptions import ClientError

import lambda_function


class TestLambdaFunction(unittest.TestCase):
    
    @patch('lambda_function.boto3.client')
    def test_lambda_handler_success(self, mock_boto_client):
        # Mock S3 client and response
        mock_s3 = MagicMock()
        mock_boto_client.return_value = mock_s3
        mock_s3.get_object.return_value = {
            'Body': MagicMock(read=MagicMock(return_value=json.dumps([
                {
                    "title": "completed",
                    "count": 80,
                    "percent": 6,
                    "trend": "down"
                },
                {
                    "title": "In Progress",
                    "count": 10,
                    "percent": 6,
                    "trend": "down"
                },
                {
                    "title": "Not Started",
                    "count": 30,
                    "percent": 10,
                    "trend": "up"
                }
            ]).encode('utf-8')))
        }
        
        event = {}
        context = {}

        response = lambda_function.lambda_handler(event, context)
        self.assertEqual(response['statusCode'], 200)
        self.assertIn('body', response)
        data = json.loads(response['body'])
        self.assertIsInstance(data, list)
        self.assertEqual(data[0]['title'], 'completed')

    @patch('lambda_function.boto3.client')
    def test_lambda_handler_failure(self, mock_boto_client):
        # Mock S3 client and exception
        mock_s3 = MagicMock()
        mock_boto_client.return_value = mock_s3
        mock_s3.get_object.side_effect = ClientError(
            {"Error": {"Code": "NoSuchKey", "Message": "The specified key does not exist."}},
            'GetObject'
        )

        event = {}
        context = {}

        response = lambda_function.lambda_handler(event, context)
        self.assertEqual(response['statusCode'], 500)
        self.assertIn('body', response)
        data = json.loads(response['body'])
        self.assertIn('error', data)
        self.assertTrue(data['error'].startswith('An error occurred'))

if __name__ == '__main__':
    unittest.main()
