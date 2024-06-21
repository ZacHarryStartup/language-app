import argparse
import os

def main(folderName, functionName):
    if not os.path.exists('lambda-functions/' + folderName):
        os.makedirs('lambda-functions/' + folderName)
    pythonFile = open('lambda-functions/' + folderName + functionName + '.py', "w")
    pythonContent = """import boto3
import json

# define the DynamoDB table that Lambda will connect to
tableName = "lambda-apigateway"

# create the DynamoDB resource
dynamo = boto3.resource('dynamodb').Table(tableName)

print('Loading function')

def lambda_handler(event, context):
    return
    """
    pythonFile.write(pythonContent)

def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f",
        "--functionName",
        required=True
    )
    parser.add_argument(
        "-f",
        "--folderName",
        required=True
    )
    return parser.parse_args()


if __name__ == "__main__":
    main(parseArgs().folderName, parseArgs().functionName)