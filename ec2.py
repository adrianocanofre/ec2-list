import boto3, sys, os
import argparse
import termtables as tt

EC2_AWS_PROFILE = os.getenv('EC2_AWS_PROFILE', 'default')
EC2_AWS_REGION = os.getenv('EC2_AWS_REGION', 'eu-central-1')


session = boto3.Session(profile_name=EC2_AWS_PROFILE)
ec2_client = session.client("ec2", region_name=EC2_AWS_REGION)

def volume_size(ids):
    volumes = ec2_client.describe_volumes(VolumeIds=ids)
    size = 0
    for id in volumes["Volumes"]:
        size += id["Size"]
    return int(size)

def get_tag(tags, key='Name'):
    if not tags: return ''
    for tag in tags:
        if tag['Key'] == key:
            return tag['Value']
    return ''

def main():

    parser = argparse.ArgumentParser()
   
    parser.add_argument('-n', default='*')
    parser.add_argument('-s', default=True, choices=['ASC', 'DESC'])

    args = parser.parse_args()

    if args.n:
        name = args.n
    if args.s:
        sort = True if args.s == 'ASC' else False
        
    running_instances = ec2_client.describe_instances(Filters=[
            {
                "Name": "tag:Name",
                "Values": [name]
            }
        ]).get("Reservations")

    ec2info = []
    for instances in running_instances:
        for instance in instances["Instances"]:
            public_ip = "---"
            if instance.get(u'PublicIpAddress') is not None:
                public_ip = instance["PublicIpAddress"]

            volumes_ids = []
            for ebs in instance["BlockDeviceMappings"]:
                volumes_ids.append(ebs["Ebs"]["VolumeId"])

            ec2info.append({
                'Name' : get_tag(instance["Tags"]), 
                'Instance ID': instance["InstanceId"],
                'Instance Type': instance["InstanceType"],
                'Private IP': instance["PrivateIpAddress"],
                'Public IP' : public_ip,
                'Size' :  volume_size(volumes_ids),
                'Status' : instance["State"]["Name"]
                })
    
    ec2info = sorted(ec2info, key=lambda x: x['Size'], reverse=sort)
    attributes = [ 'Instance Type', 'Status', 'Instance ID', 'Private IP', 'Public IP', 'Size']
    
    for instance in ec2info:
        print(instance['Name'].center(40, ' '))
        for key in attributes:
            print('| {} | {} |'.format(key.ljust(15, ' '), str(instance[key]).ljust(20, ' ') ))
        print('\n')

if __name__ == "__main__":
   main()