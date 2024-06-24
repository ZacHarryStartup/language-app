import base64
import json
import os
from openai import OpenAI
import difflib

def compareStrings(goal_sentence, attempt_sentence):
    # Split sentences into words
    goal_words = goal_sentence.split()
    attempt_words = attempt_sentence.split()

    # Create a SequenceMatcher object
    s = difflib.SequenceMatcher(None, goal_words, attempt_words)

    # Get the matching blocks
    matches = s.get_matching_blocks()

    # Reconstruct the attempt sentence based on matching words
    result_words = []
    attempt_index = 0

    for match in matches:
        # Skip unmatched words in attempt_words
        while attempt_index < match.b:
            attempt_index += 1

        # Add matching words to result
        for i in range(match.size):
            if attempt_index < len(attempt_words):
                result_words.append(attempt_words[attempt_index])
                attempt_index += 1

    # Join the result words into a modified sentence
    modified_sentence = ' '.join(result_words)

    # Reconstruct the final sentence with underscores for missing words
    final_result = []
    modified_words = modified_sentence.split()
    mod_index = len(modified_words) - 1
    goal_index = len(goal_words) - 1

    while goal_index >= 0:
        if mod_index >= 0 and goal_words[goal_index] == modified_words[mod_index]:
            final_result.append(modified_words[mod_index])
            mod_index -= 1
        else:
            underscores = "_" * len(goal_words[goal_index])
            final_result.append(underscores)
        goal_index -= 1

    # The result is built in reverse order, so reverse it back
    final_result.reverse()
    final_modified_sentence = ' '.join(final_result)
    
    return final_modified_sentence

def lambda_handler(event, context):
    try:
        # Retrieve the OpenAI API key from environment variables
        print(event['body']['goalSentence'])
        openai_api_key = os.getenv('OPENAI_API_KEY')
        if not openai_api_key:
            return {
                'statusCode': 500,
                'body': json.dumps('OpenAI API key not found in environment variables')
            }

        # Check if the request contains the base64-encoded .m4a body
        if 'body' in event:
            # Decode the base64-encoded .m4a data
            audio_data = base64.b64decode(event['body']['audioData'])
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

        client = OpenAI(api_key=openai_api_key)
        with open(audio_file_path, 'rb') as audio_file:
            transcript = client.audio.transcriptions.create(model="whisper-1", file=audio_file)

        # Return the transcript
        return {
            'statusCode': 200,
            'body': json.dumps({'transcript': transcript.text, 'compareString': compareStrings(event['body']['goalSentence'])})
        }

    except Exception as e:
        # Log the error for debugging
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }