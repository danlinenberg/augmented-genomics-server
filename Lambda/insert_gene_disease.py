from __future__ import print_function

import json
import boto3
import csv
import time
import threading
import boto3.dynamodb

print('Loading function')

    
def lambda_handler(event, context):
    global key
    gene = event["gene"]
    disease = event["disease"]
    score = event["score"]
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table("Gene_Disease")
    try:
        table.put_item(Item={
                            'Gene': gene,
                            'Disease': disease,
                            'Score': score
                            })
    except Exception as e:
        return e
        
    return "Success"
