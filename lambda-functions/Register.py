import json
import boto3
from botocore.exceptions import BotoCoreError, ClientError

# Initialize Cognito client
cognito_client = boto3.client('cognito-idp', region_name='ap-southeast-2')
user_pool_id = 'ap-southeast-2_CGcEJ2Fcb'
client_id = '5uer2o6e6atje9f29se6q4t029'

def register(event, context):
    try:
        # Directly parse event['body'] assuming it's a JSON string
        data = json.loads(event.get('body', '{}'))
        
        # Extract the required fields from the JSON data
        username = data['username']
        password = data['password']
        email = data['email']
        
        # Perform the Cognito sign-up
        response = cognito_client.sign_up(
            ClientId=client_id,
            Username=username,
            Password=password,
            UserAttributes=[
                {'Name': 'email', 'Value': email},
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
    except (KeyError, json.JSONDecodeError) as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid input data', 'message': str(e)})
        }
