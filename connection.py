import boto3

session=boto3.Session(profile_name='famc-legacy')
client=session.resource('ec2', region_name='us-east-1')

print(dir(client))
print(type(client))
