# get_sec_groups.py 

Script iterates over ec2 list and creates a set of security groups in use.
Then runs a check against a list containing all security groups, thus 
determinining which security groups are not used.

Requires IAM role or access/secret key. 

**required packages**
 - boto3



