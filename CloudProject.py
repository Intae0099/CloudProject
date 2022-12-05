import boto3

def menu():
    print("------------------------------------------------------------")
    print("1. list instance \t2. available zones")
    print("3. start instance \t4. available regions")
    print("5. stop instance \t6. create instance")
    print("7. reboot instance \t8. list images")
    print("9. credits instance 10. list tags")
    print("\t\t\t\t\t99. quit")
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

ACCESS_KEY = input("AWS_ACCESS_KEY_ID : ")
SECRET_KEY = input("AWS_SECRET_ACCESS_KEY_ID : ")

ec2_client = boto3.client('ec2', region_name='ap-northeast-1', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
ec2_resource = boto3.resource('ec2', region_name='ap-northeast-1', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
ec2_session = boto3.Session(aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
  
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
    if menu_num == 99:
        print("Quit")
        break
    elif menu_num is not None:
        print("\nSelect again")
