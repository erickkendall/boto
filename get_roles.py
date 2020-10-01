import boto3

session = boto3.Session(profile_name='272')
iam_client=session.client('iam')
response = iam_client.list_roles()
count=1
while response:
  print( str(count) + "." + " " + str(response['Roles']))
  count += 1
