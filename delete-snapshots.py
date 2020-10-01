import boto3
import datetime

accounts =  ['133','202','230','272','353','439']


for account in accounts:

  if [ account == '272' ]:
    ownerid = "097856158272"
  if [ account == '202' ]:
    ownerid = "557027395202"
  if [ account == '230' ]:
    ownerid = "693538057230"
  if [ account == '439' ]:
    ownerid = "926668386439"
  if [ account == '133' ]:
    ownerid = "647523064133"
  if [ account == '353' ]:
    ownerid = "858737304353"

  print ("account: " + account)

  boto3.setup_default_session(profile_name=account)
  client = boto3.client('ec2',region_name='us-east-1')
  snapshots = client.describe_snapshots(OwnerIds=[ownerid])
  size = 0
  count = 0
  for snapshot in snapshots ['Snapshots']:
    snapshot_time=snapshot['StartTime'].date()
    current_time=datetime.datetime.now().date()
    diff_time = current_time - snapshot_time
    size = size + snapshot['VolumeSize']
    count += 1
   
  
  
    if diff_time.days > 180:
      id = str(snapshot['SnapshotId'])
      print(account + " -- " + id + " -- " + str(snapshot_time))
  
  print( account)
  print (size)
  print (count)
