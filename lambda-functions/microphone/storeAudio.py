import base64
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

        # Check if the request contains the base64-encoded .m4a body
        if 'body' in event:
            # Decode the base64-encoded .m4a data
            audio_data = base64.b64decode(event['body'])
            print(f"Received base64 encoded audio data of length: {len(audio_data)} bytes")
        else:
            return {
                'statusCode': 400,
                'body': json.dumps('No audio file found in request')
            }

        # Define the path to save the .m4a audio file
        audio_file_path = '/tmp/audio.m4a'
        
        # Write the binary data directly to the .m4a file
        with open(audio_file_path, 'wb') as audio_file:
            audio_file.write(audio_data)
            print(f"Audio file written to: {audio_file_path}")

        client = openai.OpenAI(api_key="sk-proj-FeXYZfbbwupEo7KpLtNIT3BlbkFJGIfLI7JZqGGK8abz2WoP")

        with open(audio_file_path, 'rb') as audio_file:
            transcription = client.audio.transcriptions.create(
                model="whisper-1", 
                file=audio_file,
            )

        # Return the transcript
        return {
            'statusCode': 200,
            'body': json.dumps({'transcript': transcription['text']})
        }

    except Exception as e:
        # Log the error for debugging
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }