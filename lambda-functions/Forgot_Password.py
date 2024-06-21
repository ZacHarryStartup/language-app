from flask import Flask, request, jsonify
import boto3
from botocore.exceptions import BotoCoreError, ClientError

# Initialize Cognito client
cognito_client = boto3.client('cognito-idp', region_name='your-region')  # Replace 'your-region' with your AWS region
user_pool_id = 'your-user-pool-id'  # Replace with your Cognito User Pool ID
client_id = 'your-client-id'  # Replace with your Cognito App Client ID

#@app.route('/forgot-password', methods=['POST'])
def forgot_password():
    try:
        data = request.json
        response = cognito_client.forgot_password(
            ClientId=client_id,
            Username=data['username']
        )
        return jsonify(response), 200
    except ClientError as e:
        return jsonify(error=str(e)), 400