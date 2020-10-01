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


  session = boto3.Session(profile_name=account)
  client = session.client('iam')

  response = client.list_roles()
  for i in response ['Roles']:
    role = i['RoleName']
    response = client.generate_service_last_accessed_detail( arn:aws:iam::097856158272:role\role)
