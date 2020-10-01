import boto3
import datetime


boto3.setup_default_session(profile_name='272')
client = boto3.client('lambda', region_name='us-east-1')

lst = client.list_functions()
for x in (lst['Functions']):
  print (x['FunctionName'])
