from __future__ import print_function
import json
import boto3
import cfnresponse


SUCCESS = "SUCCESS"
FAILED = "FAILED"

print('Loading Function')
s3 = boto3.resource('s3')

def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))
    response_data = {}
    try:
        print("Request Type: ", event['RequestType'])
        if event['RequestType'] == 'Create':
            lambda_arn = event['ResourceProperties']['LambdaArn']
            bucket = event['ResourceProperties']['Bucket']
            bucket_notification = s3.BucketNotification(bucket)
            bucket_notification.put(
                NotificationConfiguration={
                    'LambdaFunctionConfigurations': [
                        {
                            'LambdaFunctionArn': lambda_arn,
                            'Events': [
                                's3:ObjectCreated:*'
                            ]
                        }
                    ]
                }
            )
            print("Put request completed....")
            response_data = {'Bucket': bucket}
            print("Sending response to custom resource")
        response_status = SUCCESS
    except Exception as e:
        print("Failed to process:", e)
        response_status = FAILED
        response_data = {'Failure': 'Something bad happened.'}
    
    cfnresponse.send(event, context, response_status, response_data)
    
