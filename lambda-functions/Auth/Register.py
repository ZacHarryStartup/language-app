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

        # Check if email and profile are already in use
        email_profile_filter = f'email="{data["email"]}"'
        existing_users = cognito_client.list_users(
            UserPoolId=user_pool_id,
            Filter=email_profile_filter
        )
        
        for user in existing_users['Users']:
            for attribute in user['Attributes']:
                if attribute['Name'] == 'profile' and attribute['Value'] == data['profile']:
                    return {
                        'statusCode': 400,
                        'body': json.dumps({'error': 'Looks like that email is already in use.'})
                    }

        # Check if username is already in use
        username_filter = f'username="{data["username"]}"'
        existing_users = cognito_client.list_users(
            UserPoolId=user_pool_id,
            Filter=username_filter
        )
        
        if existing_users['Users']:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Looks like that username is taken.'})
            }

        # Create the new user
        response = cognito_client.sign_up(
            ClientId=client_id,
            Username=data['username'],
            Password=data['password'],
            UserAttributes=[
                {'Name': 'email', 'Value': data['email']},
                {'Name': 'profile', 'Value': data['profile']},
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
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
