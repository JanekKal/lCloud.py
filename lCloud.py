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


def upload_file(local_file_path, s3_file_name):
    try:
        s3.upload_file(local_file_path, BUCKET_NAME, PREFIX + s3_file_name)
        print(f"Uploaded {local_file_path} to {PREFIX + s3_file_name}")
    except FileNotFoundError:
        print("The file was not found.")
    except NoCredentialsError:
        print("Credentials not available.")
    except ClientError as e:
        print(f"Error uploading file: {e}")

def list_files_with_filter(regex_pattern):
    try:
        response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=PREFIX)
        if 'Contents' in response:
            for obj in response['Contents']:
                if re.match(regex_pattern, obj['Key']):
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
    elif command == "upload" and len(sys.argv) == 4:
        local_file_path = sys.argv[2]
        s3_file_name = sys.argv[3]
        upload_file(local_file_path, s3_file_name)
    elif command == "list-filter" and len(sys.argv) == 3:
        regex_pattern = sys.argv[2]
        list_files_with_filter(regex_pattern)
    else:
        print("Invalid command or arguments. Available commands: list, upload, list-filter, delete-filter")

if __name__ == "__main__":
    main()