import boto3
import json
from openai import OpenAI
client = OpenAI(api_key="sk-proj-FeXYZfbbwupEo7KpLtNIT3BlbkFJGIfLI7JZqGGK8abz2WoP")




# define the DynamoDB table that Lambda will connect to
tableName = "lambda-apigateway"

# create the DynamoDB resource
dynamo = boto3.resource('dynamodb').Table(tableName)

print('Loading function')

def lambda_handler(event, context):
    
    return "Lets pretend this is stored"
    