from __future__ import print_function

import json
import boto3
import csv
import time
import threading

print('Loading function')

    
def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2)
    global key
    key = event["Key"]
    s3key = key+".csv"
    bucket = "s3-tau-bucket-vcf"
    temp = "/tmp/vcf.csv"
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table("VCF")

    return putInTable(table, s3key, bucket, temp)

def putInTable(table, s3key, bucket, temp):
    try:
        resource = boto3.resource('s3')        
        resource.Object(bucket, s3key).download_file(temp)
    except Exception as e:
        return "No VCF found for patient ID"
        
    with open(temp, 'rb') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                response = boto3.client('lambda').invoke(
                    FunctionName='find_gene_score',
                    InvocationType='RequestResponse',
                    Payload=json.dumps({"Key": row['Gene.refGene']})
                )
                row['score'] = response['Payload'].read()
                row['id'] = key
                
                table.put_item(Item=row)
                
            except Exception as e:
                print(e)
                return "Bad VCF Format"
        return "Success"
