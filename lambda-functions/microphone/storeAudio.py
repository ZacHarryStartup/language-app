import base64
import json
import os
import subprocess
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

        # Define paths for the .m4a and .wav files
        audio_file_path = '/tmp/audio.m4a'
        wav_file_path = '/tmp/audio.wav'
        
        # Write the binary data to the .m4a file
        with open(audio_file_path, 'wb') as audio_file:
            audio_file.write(audio_data)
            print(f"Audio file written to: {audio_file_path}")

        # Convert .m4a to .wav using ffmpeg
        ffmpeg_cmd = [
            '/opt/bin/ffmpeg',  # Path to ffmpeg, adjust if using a different path
            '-i', audio_file_path,
            wav_file_path
        ]

        result = subprocess.run(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            print(f"ffmpeg error: {result.stderr.decode()}")
            return {
                'statusCode': 500,
                'body': json.dumps('ffmpeg failed to convert the audio file')
            }

        print(f"Audio file converted to: {wav_file_path}")

        # Transcribe the audio using OpenAI Whisper
        openai.api_key = openai_api_key  # Use API key from environment variable
        with open(wav_file_path, 'rb') as audio_file:
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