import base64
import json
import os
import boto3
from datetime import datetime

def lambda_handler(event, context):
    try:
        # Retrieve environment variables
        s3_bucket_name = os.getenv('S3_BUCKET_NAME')
        if not s3_bucket_name:
            return {
                'statusCode': 500,
                'body': json.dumps('S3 bucket name not found in environment variables')
            }

        # Check if the request contains the base64-encoded .m4a body
        if 'body' in event:
            base64_audio_str = event['body']
            
            # Decode the base64-encoded .m4a data
            try:
                audio_data = base64.b64decode(base64_audio_str)
                print(f"Received base64 encoded audio data of length: {len(audio_data)} bytes")
            except base64.binascii.Error as decode_error:
                print(f"Error decoding base64: {decode_error}")
                return {
                    'statusCode': 400,
                    'body': json.dumps('Invalid base64 encoding')
                }
        else:
            return {
                'statusCode': 400,
                'body': json.dumps('No audio file found in request')
            }

        # Define the S3 object key (name)
        timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
        s3_object_key = f'audio_{timestamp}.m4a'
        
        # Upload the binary data to S3
        s3 = boto3.client('s3')
        try:
            s3.put_object(Bucket=s3_bucket_name, Key=s3_object_key, Body=audio_data, ContentType='audio/mp4')
            print(f"Audio file uploaded to S3 bucket '{s3_bucket_name}' with key '{s3_object_key}'")
        except Exception as e:
            print(f"Error uploading to S3: {e}")
            return {
                'statusCode': 500,
                'body': json.dumps(f'Error uploading to S3: {e}')
            }

        # Return success response with S3 file URL
        s3_file_url = f'https://{s3_bucket_name}.s3.amazonaws.com/{s3_object_key}'
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'File uploaded successfully', 'file_url': s3_file_url})
        }

    except Exception as e:
        # Log the error for debugging
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }