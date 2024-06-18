import argparse
import os

def main(functionName):
    f = open('lambda-functions/' + functionName + '.py', "w")
    fileContent = """import boto3
import json

# define the DynamoDB table that Lambda will connect to
tableName = "lambda-apigateway"

# create the DynamoDB resource
dynamo = boto3.resource('dynamodb').Table(tableName)

print('Loading function')

def lambda_handler(event, context):
    return
    """
    f.write(fileContent)
    test = open('lambda-functions/' + functionName + '.py', "r")
    print(test.read())

def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f",
        "--functionName",
        required=True
    )
    return parser.parse_args()


if __name__ == "__main__":
    main(parseArgs().functionName)