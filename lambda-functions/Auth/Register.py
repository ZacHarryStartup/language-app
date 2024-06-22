import json
import boto3
from botocore.exceptions import BotoCoreError, ClientError

# Initialize Cognito client
cognito_client = boto3.client('cognito-idp', region_name='ap-southeast-2')
user_pool_id = 'ap-southeast-2_CGcEJ2Fcb'
client_id = '5uer2o6e6atje9f29se6q4t029'

def lambda_handler(event, context):
    try:
        # Directly parse event assuming it's a JSON payload
        data = json.loads(event.get('body', '{}'))
        
        response = cognito_client.sign_up(
            ClientId=client_id,
            Username=data['username'],
            Password=data['password'],
            UserAttributes=[
                {'Name': 'email', 'Value': data['email']},
            ]
        )
        return {
            'statusCode': 200,
            'body': json.dumps(response)
        }
    except ClientError as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': str(e)})
        }
