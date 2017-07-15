from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr

# Helper class to convert a DynamoDB item to JSON.
def lambda_handler(event, context):
    
    key = event['Key']
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table("VCF")
    # What Filter we are using (see boto3.dynamodb.conditions for api)
    fe = Attr("Chr").eq("14") & Attr("1000g2014oct_eur").gte("0.003") & Attr("id").eq(key)
    # What values we what to display
    pe = "#gen, #eur, Chr"
    # Expression Attribute Names for Projection Expression only - doesn't work on Filter! (subtitution for headers with numbers or special characters)
    ean = { "#gen" : "Gene.refGene", "#eur": "1000g2014oct_eur" }

    response = table.scan(
        FilterExpression=fe,
        ProjectionExpression=pe,
        ExpressionAttributeNames=ean
    )
    
    lst = []
    for i in response['Items']:
        lst.append(i["Gene.refGene"])

    print(lst)
    return lst
