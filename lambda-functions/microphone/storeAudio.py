import boto3
import json
from openai import OpenAI
client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])




# define the DynamoDB table that Lambda will connect to
tableName = "lambda-apigateway"

# create the DynamoDB resource
dynamo = boto3.resource('dynamodb').Table(tableName)

print('Running audio function')

def lambda_handler(event, context):
    # audio_file= open("audio.m4a", "rb")
    # transcription = client.audio.transcriptions.create(
    # model="whisper-1", 
    # file=audio_file,
    # )
    # print(event, context)
    # message = {
    #     'message': transcription.text
    # }
    message = {
        'message': "hi"
    }
    # print(transcription.text)
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(message)
    }
    