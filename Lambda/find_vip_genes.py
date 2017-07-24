from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr
from  __builtin__ import any as b_any

# Helper class to convert a DynamoDB item to JSON.
def lambda_handler(event, context):
    
    id = str(event['id'])
    drug = str(event['Key'])
    dynamodb = boto3.resource('dynamodb')
    table_vcf = dynamodb.Table("VCF")
    table_vip = dynamodb.Table("GenesVIP")
    
    #VCF
    fe = Attr("id").eq(id)
    pe = "#gen"
    ean = { "#gen" : "Gene.refGene" }
    response_vcf = table_vcf.scan(
        FilterExpression=fe,
        ProjectionExpression=pe,
        ExpressionAttributeNames=ean
        )
    lst_vcf = []
    for i in response_vcf['Items']:
        lst_vcf.append(i["Gene.refGene"])

    pe_vip = "#drugs, #gen"
    ean_vip = { "#drugs" : "drugs", "#gen" : "Gene.refGene" }
    response_vip = table_vip.scan(
            # FilterExpression=fe_vip,
            ProjectionExpression=pe_vip,
            ExpressionAttributeNames=ean_vip
    )
    dict_vip = {}
    for i in response_vip['Items']:
        dict_vip[i["Gene.refGene"]] = i["drugs"]
        
    #check them both for similarities
    dict_similar = {}
    for key, value in dict_vip.iteritems():
        if key in lst_vcf:
            dict_similar[key] = value

    print(dict_similar)
    for key,value in dict_similar.iteritems():
        for word in drug:
            if((str(word).lower() in str(value).lower()) or (str(value).lower() in str(word).lower())):
                return key
    
    return False