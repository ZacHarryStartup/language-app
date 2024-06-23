import base64
import json
import os
import openai
from io import BytesIO

def lambda_handler(event, context):
    try:
        # Retrieve the OpenAI API key from environment variables
        openai_api_key = os.getenv('OPENAI_API_KEY')
        if not openai_api_key:
            return {
                'statusCode': 500,
                'body': json.dumps('OpenAI API key not found in environment variables')
            }

        # Check if the request contains the raw binary body
        if 'body' in event:
            # Handle the raw binary data directly (it's octet-stream)
            audio_data = event['body'].encode('latin1')
            print(f"Received audio data of length: {len(audio_data)} bytes")
        else:
            return {
                'statusCode': 400,
                'body': json.dumps('No audio file found in request')
            }

        # Base64 encode the audio data
        base64_audio_data = base64.b64encode(audio_data).decode('utf-8')

        # Decode the base64-encoded string back into bytes
        audio_bytes = base64.b64decode(base64_audio_data)

        # Create a file-like object from the bytes
        audio_file = BytesIO(audio_bytes)
        audio_file.name = 'audio.m4a'  # Set a name attribute as required by some APIs

        # Call OpenAI Whisper with the file-like object
        openai.api_key = openai_api_key
        transcript = openai.Audio.transcribe("whisper-1", audio_file)

        # Return the transcript
        return {
            'statusCode': 200,
            'body': json.dumps({'transcript': transcript['text']})
        }

    except Exception as e:
        # Log the error for debugging
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }