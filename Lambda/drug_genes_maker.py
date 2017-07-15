from __future__ import print_function

import json
import boto3
import csv
import time
import threading
import urllib2

print('Loading function')

    
def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2)
    global key
    key = event["Key"]
    #CSV file in S3 with VIP Gene codes
    s3key = key+".csv"
    bucket = "s3-tau-bucket-general"
    temp = "/tmp/temp.csv"
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table("GenesVIP")

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
                row['Is VIP'] = key
                drugs = []
                response = urllib2.urlopen('http://dgidb.genome.wustl.edu/api/v1/interactions.json?genes=' + row['Gene.refGene'])
                string = response.read().decode('utf-8')
                json_obj = json.loads(string)
                matchedTerms = json_obj['matchedTerms']
                response.close()
                for obj in matchedTerms:
                    for obj_in in obj['interactions']:
                        drugs.append(obj_in['drugName'])
                
                newRow = {}
                newRow['Gene.refGene'] = row['Gene.refGene']
                newRow['drugs'] = drugs
                table.put_item(Item=newRow)
                
            except Exception as e:
                return e
        return "Success"
