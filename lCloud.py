import boto3
import re
import os
import sys
from botocore.exceptions import NoCredentialsError, ClientError


def list_files():
    try:
        response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=PREFIX)
        if 'Contents' in response:
            for obj in response['Contents']:
                print(obj['Key'])
        else:
            print("No files found.")
    except ClientError as e:
        print(f"Error fetching files: {e}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python lCloud.py <command> [args]")
        return

    command = sys.argv[1]

    if command == "list":
        list_files()
    else:
        print("Invalid command or arguments. Available commands: list, upload, list-filter, delete-filter")

if __name__ == "__main__":
    main()