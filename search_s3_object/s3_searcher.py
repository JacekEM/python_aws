import argparse
import collections
import re

import boto3
import botocore


def get_buckets_iter(boto3_response):
    """
    :param boto3_response:
    :return: list containing all the buckets on the given account.
    """
    return iter([bucket_name["Name"] for bucket_name in boto3_response["Buckets"]])


def filter_bucket(bucket, search_pattern):
    """
    Overly complicated fuction to return bucket + object if object is found in the bucket
    :param bucket:
    :return named_tuple containing buckets and matching objects
    :search_patter string that is searched for in buckets
    """

    # search_pattern = "corretto"
    try:
        location = collections.namedtuple('location', 'bucket object')
        result = location(bucket=bucket,
                          object=list(filter(lambda match: re.match(".*" + search_pattern + ".*", str(match["Key"])),
                                             client.list_objects(Bucket=bucket)["Contents"])))

        if result.object:
                print(f"\"{str(getattr(result, 'bucket'))}\" bucket contains the following object(s):\n \
                        {[ obj['Key'] for obj in getattr(result, 'object')]}\n\n")

    except KeyError:
        pass
            # print(bucket + " is empty")

    except botocore.exceptions.ClientError as err:
        print(str(err) + f" on {bucket} bucket")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-profile", help="aws profile to use")
    parser.add_argument("-pattern", help="patters to search on s3 buckets")
    args = parser.parse_args()
    session = boto3.Session(profile_name=args.profile)
    client = session.client('s3')

    buckets = get_buckets_iter(client.list_buckets())

    try:
        while buckets.__next__():
            filter_bucket(next(buckets), args.pattern)

    except StopIteration:
        print(f"finished searching")

