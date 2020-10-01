import boto3


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
  

  s3 = boto3.client('s3')
  response = s3.list_buckets()
  buckets = [bucket['Name'] for bucket in response['Buckets']]


  print("Bucket List: %s" % buckets)
