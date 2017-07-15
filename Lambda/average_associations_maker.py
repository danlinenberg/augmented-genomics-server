from __future__ import print_function

import json
import boto3
import csv
import time
import threading
import urllib2

print('Loading function')

    
def lambda_handler(event, context):

    #CSV file in S3 with VIP Gene codes
    global key
    key = event["Key"]
    s3key = key+".csv"
    bucket = "s3-tau-bucket-general"
    temp = "/tmp/temp.csv"
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table("GeneAverageScore")

    return putInTable(table, s3key, bucket, temp)

def putInTable(table, s3key, bucket, temp):
    try:
        resource = boto3.resource('s3')        
        resource.Object(bucket, s3key).download_file(temp)
    except Exception as e:
        return e
        
    with open(temp, 'rb') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                json = dict(row)
                table.put_item(Item=json)
            except Exception as e:
                return e
        return "Success"
