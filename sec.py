import boto
ec2 = boto.connect_ec2()
sgs = ec2.get_all_security_groups()
for sg in sgs:
    print sg.name, len(sg.instances())
