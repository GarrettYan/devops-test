import json

import boto3
from botocore.exceptions import ClientError


def lambda_handler(event, context):
    # print("Hello Garrett, How are you?")

    s3 = boto3.client('s3')
    bucket_name = 'epidaurus-health-json-storage'
    file_key = 'wireframe-stat.json'

    try:
        response = s3.get_object(Bucket=bucket_name, Key=file_key)
        content = response['Body'].read().decode('utf-8')
        data = json.loads(content)
        return {
            'statusCode': 200,
            'body': json.dumps(data)
        }
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
