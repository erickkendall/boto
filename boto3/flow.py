import boto3
import re

session = boto3.Session(profile_name='famc-legacy')
client = session.client('logs', region_name='us-east-1')

response=client.describe_log_groups()

all_logs = {}
for log in response.get('logGroups'):
  log_group_name = log.get('logGroupName') 
  if 'cfg' and 'vpc' in log_group_name:
    flowlog_list = []
    all_streams = []
    stream_batch = client.describe_log_streams(logGroupName=log_group_name)
    all_streams += stream_batch['logStreams']
    while 'nextToken' in stream_batch:
      stream_batch = client.describe_log_streams(logGroupName=log_group_name,nextToken=stream_batch['nextToken'])
      all_streams += stream_batch['logStreams']
    for row in all_streams:
      flowlog_list.append(row.get('logStreamName'))
    all_logs.update({log_group_name:flowlog_list})

# all interfaces attached to an EC2 
all_server_interfaces = {}
interfacedict = {}
server_list = session.resource('ec2', region_name='us-east-1')
for server in server_list.instances.all():
    tags = server.tags
    if tags is not None:
        for tag in tags:
            if tag.get('Key') == 'Name':
                hostname = tag.get('Value')
                interfacelist = []
                for interface in server.network_interfaces:
                    interfacelist.append(interface.id)
        interfacedict.update({hostname: interfacelist})

for key in interfacedict.keys():
  interface = interfacedict.get(key)
  if len(interface) > 0:
    print(f"{key} {interface}")


key_list = list(all_logs.keys())
for row in key_list:
  print(len(all_logs.get(row)))
