#!/usr/bin/env python

import boto3, logging

# Setup Logging
logger = logging.getLogger('ec2ctrl.py')
hdlr = logging.FileHandler('/var/log/ec2ctrl.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)


# .aws\credentials profiles to loop through - configure regions in credentials file - region = us-east-1 etc
profiles = ["imagingqa", "imagingdev", "mobiledev", "dataservicesdev", "dataservicesqa", "javastacksdev"]

# Loop through profiles and perform shutdown
for i in profiles:
    profile = i
    session = boto3.Session(profile_name = profile)
    ec2 = session.resource('ec2')
# Loop through instances on each account to find all running instances to perform shutdown on
    instances = ec2.instances.filter(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    for instance in instances:
        print("Found and shut down %s %s in %s" % (instance.id, instance.instance_type, i))
        logger.info("Found and shut down %s %s in %s" % (instance.id, instance.instance_type, i))
        instances.stop()
