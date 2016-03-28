from sys import argv
import json
import boto3

def dynamo_session(region='us-east1'):
    session = boto3.Session(profile_name='profile')
    dynamo = session.resource('dynamodb')
    return dynamo

values = json.loads(argv[1])  # Take json input
dynamo = dynamo_session()  # Init AWS DynamoDB Session
table = dynamo.Table('OSinfo')
response = table.put_item(
    Item={
        'Vendor': values['Vendor'][0],
        'Version': values['Version'][0]
    }
)