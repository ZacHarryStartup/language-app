from flask import Flask, request, jsonify
import boto3
from botocore.exceptions import BotoCoreError, ClientError

# Initialize Cognito client
cognito_client = boto3.client('cognito-idp', region_name='your-region')  # Replace 'your-region' with your AWS region
user_pool_id = 'your-user-pool-id'  # Replace with your Cognito User Pool ID
client_id = 'your-client-id'  # Replace with your Cognito App Client ID

#@app.route('/confirm-register', methods=['POST'])
def confirm_sign_up():
    try:
        data = request.json
        response = cognito_client.confirm_sign_up(
            ClientId=client_id,
            Username=data['username'],
            ConfirmationCode=data['confirmation_code']
        )
        return jsonify(response), 200
    except ClientError as e:
        return jsonify(error=str(e)), 400