import boto3
import json

def lambda_handler(event, context):
    # TODO implement
        #CREATE THE TABLE    
    key = event["Key"]
    dynamodb = boto3.resource('dynamodb')
    client = boto3.client('lambda')

    try:
        table = dynamodb.create_table(
            TableName=key,
            KeySchema=[
                {
                    'AttributeName': 'Gene.refGene',
                    'KeyType': 'HASH'  #Partition 
                }
                
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'Gene.refGene',
                    'AttributeType': 'S'  #Partition 
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }   
        )
        response = client.invoke(
            FunctionName='table_maker',
            InvocationType='RequestResponse',
            Payload=json.dumps(event)
        )
        return response['Payload'].read()
                                       
    except Exception as e:
        response = client.invoke(
            FunctionName='table_maker',
            InvocationType='RequestResponse',
            Payload=json.dumps(event)
        )
        return response['Payload'].read()
