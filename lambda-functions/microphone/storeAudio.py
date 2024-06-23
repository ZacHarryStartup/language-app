import json
import os
import openai
import base64

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
            # Handle the raw binary data directly (as octet-stream)
            audio_data = base64.b64decode(event['body'])
            print(f"Received base64 decoded audio data of length: {len(audio_data)} bytes")
        else:
            return {
                'statusCode': 400,
                'body': json.dumps('No audio file found in request')
            }

        # Define the path to save the audio file
        audio_file_path = '/tmp/audio.m4a'
        
        # Write the binary data directly to the .m4a file
        with open(audio_file_path, 'wb') as audio_file:
            audio_file.write(audio_data)
            print(f"Audio file written to: {audio_file_path}")

        # Transcribe the audio using OpenAI Whisper
        openai.api_key = openai_api_key  # Use API key from environment variable
        with open(audio_file_path, 'rb') as audio_file:
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