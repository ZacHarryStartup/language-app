from google.oauth2 import id_token
from google.auth.transport import requests
import json
import boto3
import requests as http_requests

# Constants (replace with your values)
CLIENT_ID = '970665302383-v2fp9sap9o0ql68flg0eubl9ee9oqsgb.apps.googleusercontent.com' # or is it frontend/ios client_id? 970665302383-c2oktt71mje4r4ov9u04589uk77qtejp.apps.googleusercontent.com
COGNITO_USER_POOL_ID = 'ap-southeast-2_CGcEJ2Fcb'
LOGIN_URL = 'https://01ue1t7qdf.execute-api.ap-southeast-2.amazonaws.com/Test/login'
REGISTER_URL = 'https://01ue1t7qdf.execute-api.ap-southeast-2.amazonaws.com/register'

# Initialize Cognito client
cognito_client = boto3.client('cognito-idp')

def tokenSignIn(token: str):
    try:
        # Verify Google ID token
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)

        # Extract the user's Google Account ID from the decoded token
        userid = idinfo['sub']
        email = idinfo['email']
        name = idinfo.get('name', '')

        print(f'Google ID verified: UserID: {userid}, Email: {email}, Name: {name}')
        
        # Check if the user exists in Cognito
        try:
            cognito_response = cognito_client.admin_get_user(
                UserPoolId=COGNITO_USER_POOL_ID,
                Username=email
            )
            print(f'User found in Cognito: {email}')
            
            # If user exists, sign them in via Lambda login function
            login_payload = {
                'username': email,
                'password': userid  # Assuming password is set to Google sub
            }
            login_response = http_requests.post(
                LOGIN_URL,
                headers={'Content-Type': 'application/json'},
                data=json.dumps(login_payload)
            )
            print(f'Login response: {login_response.json()}')
            return login_response.json()

        except cognito_client.exceptions.UserNotFoundException:
            print(f'User not found in Cognito, creating a new user: {email}')
            
            # Create the user via Lambda register function
            register_payload = {
                'username': email,
                'password': userid,  # Use Google sub as a unique password
                'email': email
            }
            register_response = http_requests.post(
                REGISTER_URL,
                headers={'Content-Type': 'application/json'},
                data=json.dumps(register_payload)
            )
            print(f'Register response: {register_response.json()}')
            return register_response.json()

    except ValueError:
        # Invalid token
        print('Invalid token')
        return {'error': 'Invalid token'}
    except boto3.exceptions.Boto3Error as e:
        print(f'AWS Boto3Error: {e}')
        return {'error': str(e)}

def lambda_handler(event, context):
    try:
        # Extract the token from the event
        body = json.loads(event.get('body', '{}'))
        token = body.get('token')
        if not token:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Token is missing'})
            }
        
        # Process the token and handle sign-in or registration
        response = tokenSignIn(token)
        
        return {
            'statusCode': 200,
            'body': json.dumps(response)
        }
    except Exception as e:
        print(f'Exception in lambda_handler: {e}')
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
