from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr
from  __builtin__ import any as b_any

def lambda_handler(event, context):
    
    id = int(event['Key'])
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table("Doctor")
    
    try:
        response = table.get_item(Key={'id': id})
        return response['Item']['access']
    except Exception as e:
        return 3
    