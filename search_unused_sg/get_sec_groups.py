import boto3


def main():
    """
    Main method, might take arguments one day.
    Just to start it invokes get_unused_sg function.
    """

    print(get_unused_sg())


def get_unused_sg():
    """
    Checks security groups assigned to ec2s and compares to a list
    containing all security groups.
    """

    ec2 = boto3.client('ec2')
    ec2_list = ec2.describe_instances()
    all_security_groups = ec2.describe_security_groups()
   
    assigned_sgs = [] 
    security_groups_ids = set()

    for sg in all_security_groups["SecurityGroups"]:
        security_groups_ids.add(sg["GroupId"])

    for reservation in ec2_list["Reservations"]:
        for instance in reservation["Instances"]:
            for sg in instance["SecurityGroups"]:
                assigned_sgs.append(sg["GroupId"])

    unassigned_sg = [sg for sg in security_groups_ids if sg not in assigned_sgs]
    
    return unassigned_sg


if __name__ == "__main__":
    main()
