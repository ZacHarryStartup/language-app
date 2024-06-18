import boto3
import json

# define the DynamoDB table that Lambda will connect to
tableName = "lambda-apigateway"

# create the DynamoDB resource
dynamo = boto3.resource('dynamodb').Table(tableName)

print('Loading function')

def lambda_handler(event, context):
    loginDetails = event.get('payload')
    print(loginDetails)
    response = dynamo.get_item(Item=loginDetails)

    print(response)
    print("Picklessss")




    # def ddb_create(x):
    #     print(x, **x)
    #     dynamo.put_item(**x)

    # def ddb_read(x):
    #     dynamo.get_item(**x)

    # def ddb_update(x):
    #     print(x, **x)
    #     dynamo.update_item(**x)
        
    # def ddb_delete(x):
    #     dynamo.delete_item(**x)

    # def echo(x):
    #     return x

    # operation = event['operation']

    # operations = {
    #     'create': ddb_create,
    #     'read': ddb_read,
    #     'update': ddb_update,
    #     'delete': ddb_delete,
    #     'echo': echo,
    # }

    # if operation in operations:
    #     return operations[operation](event.get('payload'))
    # else:
    #     raise ValueError('Unrecognized operation "{}"'.format(operation))