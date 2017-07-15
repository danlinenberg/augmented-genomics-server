from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr
from  __builtin__ import any as b_any

# Helper class to convert a DynamoDB item to JSON.
def lambda_handler(event, context):
    
    gene = event['Key']
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table("GeneAverageScore")

    try:
        response = table.get_item(Key={'Gene.refGene': gene})

        if(response['Item']):
            return float(response['Item']['score'])
        return 0
    except Exception as e:
        return 0
