from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr

def lambda_handler(event, context):
    try:
        dynamodb = boto3.resource('dynamodb')
        client = boto3.client('lambda')
        table_patient = dynamodb.Table("Patient")
        
        patient_id = int(event['Key'])
        treater_id = int(event['doctor'])
        request = event['request']

        treater_response = client.invoke(
            FunctionName='access_control_handler',
            InvocationType='RequestResponse',
            Payload=json.dumps({"Key": treater_id})
        )

        treater_level = int(treater_response['Payload'].read())
        
        #super-doctor
        if(treater_level==0):
            return 2
        
        request_header = "access_level_"+str(request)+str(treater_level)
        
        fe = Attr("id").eq(patient_id)
        pe = "#res"
        ean = { "#res" : request_header }
        res_patient = table_patient.scan(
            FilterExpression=fe,
            ProjectionExpression=pe,
            ExpressionAttributeNames=ean
        )
        # patient = table_patient.get_item(Key={'id': patient_id})
        # print(json.dumps(res_patient['Items']))
        for i in res_patient['Items']:
            permission = int(i[request_header])
            if(permission==2): #Full
                return 2
            if(permission==1): #Partial
                return {
                    1: 2, 
                    2: 2,
                    3: 1,
                    4: 1,
                    5: 1
                }[treater_level]
            if(permission==0): #Blocked
                return {
                    1: 1, 
                    2: 0,
                    3: 0,
                    4: 0,
                    5: 0
                }[treater_level]
            return 0
    except Exception as e:
        print(e)
        return 0
    
