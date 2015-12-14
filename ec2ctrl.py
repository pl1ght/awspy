import boto3, logging


logger = logging.getLogger('ec2ctrl.py')
hdlr = logging.FileHandler('/var/log/ec2ctrl.og')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)

profiles = ["imagingqa", "imagingdev", "javastacksdev", "mailservicesqa", "dataservicesdev", "dataservicesqa", "mobiledev"]

profile = 'imagingqa'
region = 'us-east-1'
session = boto3.Session(profile_name = profile, region_name=region)
ec2 = session.resource('ec2')

instances = ec2.instances.filter(
    Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
for instance in instances:
    logger.info("Found and shut down %s %s in %s" % (instance.id, instance.instance_type, profile))
    #instances.stop()