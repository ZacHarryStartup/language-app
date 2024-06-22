from flask import Flask, request, jsonify
import boto3
from botocore.exceptions import BotoCoreError, ClientError

# Initialize Cognito client
cognito_client = boto3.client('cognito-idp', region_name='ap-southeast-2')  # Replace 'your-region' with your AWS region
user_pool_id = 'ap-southeast-2_CGcEJ2Fcb'  # Replace with your Cognito User Pool ID
client_id = '5uer2o6e6atje9f29se6q4t029'  # Replace with your Cognito App Client ID

#@app.route('/resend-confirmation-code', methods=['POST'])
def resend_confirmation_code():
    try:
        data = request.json
        response = cognito_client.resend_confirmation_code(
            ClientId=client_id,
            Username=data['username']
        )
        return jsonify(response), 200
    except ClientError as e:
        return jsonify(error=str(e)), 400
