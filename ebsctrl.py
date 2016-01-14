#!/usr/bin/env python

import boto3, logging, json, pprint
from datetime import datetime, timedelta
import json

profile = 'imagingdev'
region = 'us-east-1'

session = boto3.Session(profile_name=profile, region_name=region)
ec2 = session.resource('ec2')
cloudwatch = session.client('cloudwatch')

today = datetime.now() + timedelta(days=1)
two_weeks = timedelta(days=14)
start_date = today - two_weeks


def get_metrics(volume_id):
    metrics = cloudwatch.get_metric_statistics(
        Namespace='AWS/EBS',
        MetricName='VolumeIdleTime',
        Dimensions=[{'Name': 'VolumeId', 'Value': volume_id}],
        Period=3600,
        StartTime=start_date,
        EndTime=today,
        Statistics=['Minimum'],
        Unit='Seconds'
    )
    return metrics['Datapoints']

def get_available_volumes():
    available_volumes = ec2.volumes.filter(
        Filters=[{'Name': 'status', 'Values': ['available']}]
    )
    return available_volumes

def is_candidate(volume_id):
    metrics = get_metrics(volume_id)
    if len(metrics):
        for metric in metrics:
            if metric['Minimum'] < 299:
                return False
    return True

#for i in get_available_volumes():
#    print i.volume_id
#    pprint.pprint(get_cloudwatch(i.volume_id))

