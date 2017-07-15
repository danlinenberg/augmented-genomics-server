from __future__ import print_function # Python 2/3 compatibility

import boto3
import json
from boto3.dynamodb.conditions import Key, Attr

def lambda_handler(event, context):
    
    key = event["Key"]
    dynamodb = boto3.resource('dynamodb')
    client = boto3.client('lambda')
    table = dynamodb.Table("VCF")

    try:
        response = table.query(
            KeyConditionExpression=Key("id").eq(key)
        )
        if(len(response['Items'])>0):
            for i in response['Items']:
                table.get_item(
                    Key={
                        'id': key,
                        'Gene.refGene': i['Gene.refGene']
                    },   
                )
                return "Data Exists"
        else:
            return insertToTable(client, event)
    except Exception as e:
            return insertToTable(client, event)

def insertToTable(client, event):
    response = client.invoke(
        FunctionName='table_maker',
        InvocationType='RequestResponse',
        Payload=json.dumps(event)
    )
    return response['Payload'].read()
