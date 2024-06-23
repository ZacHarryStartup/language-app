import json
import base64
import os
import openai

def lambda_handler(event, context):
    try:
        # Retrieve the OpenAI API key from environment variables
        openai_api_key = os.getenv('OPENAI_API_KEY')
        if not openai_api_key:
            return {
                'statusCode': 500,
                'body': json.dumps('OpenAI API key not found in environment variables')
            }

        # Check if the request contains the body
        if 'body' in event:
            # Decode the base64-encoded audio data
            audio_data = base64.b64decode(event['body'])
            print(event['body'])
        else:
            return {
                'statusCode': 400,
                'body': json.dumps('No audio file found in request')
            }

        # Save the audio data to a file in the /tmp directory
        audio_file_path = '/tmp/audio.mp3'
        with open(audio_file_path, 'wb') as audio_file:
            audio_file.write(audio_data)

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