import json
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

        # Check if the request contains the raw binary body
        if 'body' not in event:
            return {
                'statusCode': 400,
                'body': json.dumps('No audio file found in request')
            }

        transcript = openai.Audio.transcribe("whisper-1", event['body'])

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