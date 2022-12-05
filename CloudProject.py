import boto3
import time

def menu():
    print("------------------------------------------------------------")
    print("1. list instance \t2. available zones")
    print("3. start instance \t4. available regions")
    print("5. stop instance \t6. create instance")
    print("7. reboot instance \t8. list images")
    print("9. credits instance 10. list tags")
    print("11. create tags \t12. delete tags")
    print("13. send command\t99. quit")
    print("------------------------------------------------------------")
    menu_num = input("Enter an integer : ")
    return menu_num

def list_ins(ec2):
    print("Listing instances....")
    for instance in ec2.instances.all():
        if instance:
            print("[id] " + instance.id + ", [AMI] "+ instance.image_id +", [type] "
                  + instance.instance_type + ", [state] " + instance.state['Name']
                  + ", [monitoring state] " + instance.monitoring['State'])
    return

def avail_zone(ec2):
    print("Available zones....")
    zones = ec2.describe_availability_zones()
    for zone in zones['AvailabilityZones']:
        print("[id] " + zone['ZoneId'] + ",  [region]"
              + zone['RegionName'].rjust(20, " ") + ",  [zone] "
              + zone['ZoneName'].rjust(20, " "))
    return

def start_ins(ec2):
    ins_id = input("Enter Instance id: ")
    ins_list = []
    ins_list.append(ins_id)
    if ins_id is not None:
        print("Starting ... " + ins_id)
        ec2.start_instances(InstanceIds=ins_list)
        print("Successfully started instance " + ins_id)
    else:
        print("Insert Again")
    return

def avail_region(ec2):
    print("Available regions....")
    regions = ec2.describe_regions()
    for region in regions['Regions']:
        print("[region] " + region['RegionName'].rjust(20, " ")
              + ",  [endpoint] " + region['Endpoint'])
    return

def stop_ins(ec2):
    ins_id = input("Enter Instance id: ")
    ins_list = []
    ins_list.append(ins_id)
    if ins_id is not None:
        ec2.stop_instances(InstanceIds=ins_list)
        print("Successfully stop instance " + ins_id)
    else:
        print("Insert Again")
    return

def create_ins(ec2):
    ami_id = input("Enter ami id: ")
    instance = ec2.run_instances(ImageId=ami_id, InstanceType='t2.micro', MaxCount=1, MinCount=1)
    instance_id = instance['Instances'][0]
    print("Successfully started EC2 instance " + instance_id['InstanceId'] + " based on AMI "+ ami_id)
    return

def reboot_ins(ec2):
    ins_id = input("Enter Instance id: ")
    ins_list = []
    ins_list.append(ins_id)
    print("Rebooting ... " + ins_id)
    if ins_id is not None:
        ec2.reboot_instances(InstanceIds=ins_list)
        print("Successfully rebooted instance " + ins_id)
    else:
        print("Insert Again")
    return

def list_img(ec2):
    print("Listing images....")
    images = ec2.describe_images(Owners=['self'])
    if(images['Images']):
        for image in images['Images']:
            print("[ImageID] " + image['ImageId'] + ", [Name] " + image['Name'] + ", [Owner]" + image['OwnerId'])
    return

def ins_credit(ec2):                        #Information about the credit option for CPU usage of an instance.
    print("Instance credit ....")
    ins_id = input("Enter Instance id: ")
    ins_list = []
    ins_list.append(ins_id)
    credits = ec2.describe_instance_credit_specifications(InstanceIds=ins_list)
    print("[ID] " + ins_id + ", [CPU Credits] " + credits['InstanceCreditSpecifications'][0]['CpuCredits'])

def tag_list(ec2):
    tags = ec2.describe_tags()
    for tag in tags['Tags']:
        print("[Key] " + tag['Key'].rjust(10, " ") + ", [Value] " + tag['Value'].rjust(20, " ") + ", [Resource ID] " + tag['ResourceId'].rjust(25, " ") + ", [ResourceType] " + tag['ResourceType'].rjust(20, " "))

def create_tags(ec2):
    resource = input("Enter resource : ")
    key = input("Enter key : ")
    value = input("Enter value : ")
    resource_list = []
    resource_list.append(resource)
    tags_dict = {'Key':key, 'Value':value}
    tags_list = []
    tags_list.append(tags_dict)
    ec2.create_tags(Resources=resource_list, Tags=tags_list)

def del_tags(ec2):
    resource = input("Enter resource : ")
    resource_list = []
    resource_list.append(resource)
    ec2.delete_tags(Resources=resource_list)

def aws_command(ssm):
    ins_id = input("Enter Instance id: ")
    command = input("Enter command: ")
    command_response = ssm.send_command(
        InstanceIds=[ins_id],
        DocumentName="AWS-RunShellScript",
        Parameters={
            'commands': [command],
            'executionTimeout': ['3600'], },
        TimeoutSeconds=30, )
    command_id = command_response['Command']['CommandId']
    time.sleep(2)
    output = ssm.get_command_invocation(
        CommandId=command_id,
        InstanceId=ins_id,
    )
    print(output['StandardOutputContent'])

ACCESS_KEY = input("AWS_ACCESS_KEY_ID : ")
SECRET_KEY = input("AWS_SECRET_ACCESS_KEY_ID : ")

ec2_client = boto3.client('ec2', region_name='ap-northeast-1', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
ec2_resource = boto3.resource('ec2', region_name='ap-northeast-1', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
ec2_session = boto3.Session(aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
ssm = boto3.client('ssm', region_name="ap-northeast-1", aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)

while(1):
    menu_string = menu()
    menu_num = int(menu_string)
    if menu_num == 1:
        list_ins(ec2_resource)
    if menu_num == 2:
        avail_zone(ec2_client)
    if menu_num == 3:
        start_ins(ec2_client)
    if menu_num == 4:
        avail_region(ec2_client)
    if menu_num == 5:
        stop_ins(ec2_client)
    if menu_num == 6:
        create_ins(ec2_client)
    if menu_num == 7:
        reboot_ins(ec2_client)
    if menu_num == 8:
        list_img(ec2_client)
    if menu_num == 9:
        ins_credit(ec2_client)
    if menu_num == 10:
        tag_list(ec2_client)
    if menu_num == 11:
        create_tags(ec2_client)
    if menu_num == 12:
        del_tags(ec2_client)
    if menu_num == 13:
        aws_command(ssm)
    if menu_num == 99:
        print("Quit")
        break
    elif menu_num is not None:
        print("\nSelect again")