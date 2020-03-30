##########################################################################
#
#
#
#
##########################################################################
import json
import os
import boto3
import datetime
import botocore

today = datetime.date.today()

instance = os.getenv('instance')
region = os.getenv("region")
subnet_group = os.getenv('subnet_group')
retention = os.getenv('retention')
snapshot_prefix = os.getenv('snapshot_prefix')
task = os.getenv('task')

print(task)

client = boto3.client('redshift')


def lambda_handler(event, context):

    response = client.describe_cluster_snapshots()
    #
    # is there a snapshot of the instance
    #
    snapshot_list = []

    # check if instance has a snapshot
    for snapshot in response.get('Snapshots'):
        if instance == snapshot.get('ClusterIdentifier'):
            snapshot_list.append(snapshot.get('SnapshotIdentifier'))

    if task == "delete":
        # verify recent snapshots
        if len(snapshot_list) >= 0:
            we_can_delete = 'false'
            if snapshot_prefix + today.strftime("%Y%m%d") in snapshot_list:
                print('We have a snapshot from, today.')
                we_can_delete = 'true'
            else:
                print('Let\'s get a snapshot.')
                try:
                    response = client.create_cluster_snapshot(
                        SnapshotIdentifier=snapshot_prefix +
                        today.strftime("%Y%m%d"),
                        ClusterIdentifier=instance,
                        ManualSnapshotRetentionPeriod=int(retention))
                except botocore.exceptions.ClientError as error:
                    e = error
                    print(e)
                    if e:
                        if error.response['Error']['Code'] == 'ClusterNotFound':
                            print('Cluster not found!')
                        elif error.response['Error']['Code'] == 'InvalidClusterState':
                            print('Invalid Cluster State')
                        else:
                            print('Unknown error.')

        if we_can_delete == 'true':
            print("Delete cluster.")
            try:
                response = client.delete_cluster(
                    ClusterIdentifier=instance,
                    SkipFinalClusterSnapshot=True
                )
            except botocore.exceptions.ClientError as error:
                e = error
                print(e)
                if e:
                    if error.response['Error']['Code'] == 'ClusterNotFound':
                        print('Cluster not found!')
                    else:
                        print('Unknown error.')

    if task == 'create':
        if len(snapshot_list) >= 0:
            recent_snapshot_found = 'false'
            for count in range(0, 7, 1):
                prior = today - datetime.timedelta(days=count)
                print(prior)
                if snapshot_prefix + prior.strftime("%Y%m%d") in snapshot_list:
                    recent_snapshot_found = 'true'
                    break
        if recent_snapshot_found == 'true':
            try:
                response = client.restore_from_cluster_snapshot(
                    ClusterIdentifier=instance,
                    SnapshotIdentifier=snapshot_prefix +
                    prior.strftime("%Y%m%d"),
                    ClusterSubnetGroupName=subnet_group)
            except botocore.exceptions.ClientError as error:
                e = error
                if error.response['Error']['Code'] == 'ClusterAlreadyExists':
                    print('Cluster already exists.')
        else:
            print('Recent snapshot not found.')
