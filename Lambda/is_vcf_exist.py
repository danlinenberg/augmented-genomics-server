from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr
from  __builtin__ import any as b_any

# Helper class to convert a DynamoDB item to JSON.
def lambda_handler(event, context):
    
    id = event['Key']
    dynamodb = boto3.resource('dynamodb')
    table_vcf = dynamodb.Table("VCF")
    
    #VCF
    fe = Attr("id").eq(id)
    pe = "#gen"
    ean = { "#gen" : "Gene.refGene" }
    response_vcf = table_vcf.scan(
        FilterExpression=fe,
        ProjectionExpression=pe,
        ExpressionAttributeNames=ean
        )
    if(response_vcf['Count']>0):
        return 'true'
    return 'false'

    
