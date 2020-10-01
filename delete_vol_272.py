import boto3
import datetime

boto3.setup_default_session(profile_name='353')
client = boto3.client('ec2',region_name='us-east-1')
snapshots = client.describe_snapshots(OwnerId=['858737304353'])


for snapshot in snapshots['Snapshots']:
  snapshot_time=snapshot['StartTime'].date()
  current_time=datetime.datetime.now().date()
  diff_time = current_time - snapshot_time



  if diff_time.days > 365:
    id = str(snapshot['SnapshotId'])
    print(id)
    size = size + snapshot['VolumeSize']
    count += 1

