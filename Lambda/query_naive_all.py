from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr

# Helper class to convert a DynamoDB item to JSON.
def lambda_handler(event, context):
    
    id = event['Key']
    access_allowed = int(event['access'])
    
    if(access_allowed==0):
        return "ACCESS_DENIED"
    
    client = boto3.client('lambda')
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table("VCF")
    # What Filter we are using (see boto3.dynamodb.conditions for api)
    fe = Attr("Chr").eq("14") & Attr("1000g2014oct_all").gte("0.003") & Attr("id").eq(id)
    # What values we what to display
    pe = "#gen, #eur, Chr"
    # Expression Attribute Names for Projection Expression only - doesn't work on Filter! (subtitution for headers with numbers or special characters)
    ean = { "#gen" : "Gene.refGene", "#eur": "1000g2014oct_all" }

    response = table.scan(
        FilterExpression=fe,
        ProjectionExpression=pe,
        ExpressionAttributeNames=ean
    )
    
    lst = []
    for i in response['Items']:
        gene = i["Gene.refGene"]
        response_gene = client.invoke(
            FunctionName='find_gene_score',
            InvocationType='RequestResponse',
            Payload=json.dumps({"Key": gene})
        )
    
        gene_score = float(response_gene['Payload'].read())
        #puts gene in list if the treater has access to sensitive genes
        if(access_allowed==2 or gene_score==0):
            lst.append(gene)
        else:
            lst.append("ACCESS_DENIED")
    
    return ','.join(lst)
