#Deletes patient's data

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
    except Exception as e:
        return "No data exists"

    if(len(response['Items'])>0):
        for i in response['Items']:
            try:
                table.delete_item(
                    Key={
                        'id': key,
                        'Gene.refGene': i['Gene.refGene']
                    },   
                )
            except Exception as e:
                pass
        return "Success"
    else:
        return "No data found for patient ID"