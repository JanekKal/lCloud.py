import boto3
import re
import sys
from botocore.exceptions import NoCredentialsError, ClientError

BUCKET_NAME = 'XXX'
PREFIX = 'XXX/'  #remember to add -> / <- character after specyfing the Prefix


#getting credentials from user input
def get_s3_client(access_key, secret_key):
    return boto3.client(
        's3',
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key
    )

#command list
def list_files(s3):
    try:
        response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=PREFIX)
        if 'Contents' in response:
            for obj in response['Contents']:
                print(obj['Key'])
        else:
            print("There are no files at all in the S3 bucket.")
    except ClientError as e:
        print(f"Error fetching files: {e}")


#command upload
def upload_file(s3, local_file_path, s3_file_name):
    try:
        s3.upload_file(local_file_path, BUCKET_NAME, PREFIX + s3_file_name)
        print(f"Uploaded {local_file_path} to {PREFIX + s3_file_name}")
    except FileNotFoundError:
        print("The file was not found.")
    except NoCredentialsError:
        print("Credentials not available.")
    except ClientError as e:
        print(f"Error uploading file: {e}")


#command list-filter
def list_files_with_filter(s3, regex_pattern):
    try:
        response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=PREFIX)
        matching_files = []
        
        if 'Contents' in response:
            for obj in response['Contents']:
                if re.match(regex_pattern, obj['Key']):
                    matching_files.append(obj['Key'])
                    
            if matching_files:
                for file in matching_files:
                    print(file)
            else:
                print("There are no files at all in the S3 bucket matching the regex pattern.")
        else:
            print("There are no files at all in the S3 bucket.")
            
    except ClientError as e:
        print(f"Error fetching files: {e}")


#command delete-filter
def delete_files_with_filter(s3, regex_pattern):
    try:
        response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=PREFIX)
        if 'Contents' in response:
            files_to_delete = [obj['Key'] for obj in response['Contents'] if re.match(regex_pattern, obj['Key'])]
            if files_to_delete:
                delete_objects = [{'Key': key} for key in files_to_delete]
                s3.delete_objects(Bucket=BUCKET_NAME, Delete={'Objects': delete_objects})
                print(f"Deleted files: {', '.join(files_to_delete)}")
            else:
                print("No files matched the pattern.")
        else:
            print("There are no files at all in the S3 bucket.")
    except ClientError as e:
        print(f"Error deleting files: {e}")



def main():
    if len(sys.argv) < 4:
        print("Usage: python lCloud_userInput.py <access_key> <secret_key> <command> [args]")
        return

    access_key = sys.argv[1]
    secret_key = sys.argv[2]
    command = sys.argv[3]

    # Initializing the S3 credentials
    s3 = get_s3_client(access_key, secret_key)

    if command == "list":
        list_files(s3)
    elif command == "upload" and len(sys.argv) == 6:
        local_file_path = sys.argv[4]
        s3_file_name = sys.argv[5]
        upload_file(s3, local_file_path, s3_file_name)
    elif command == "list-filter" and len(sys.argv) == 5:
        regex_pattern = sys.argv[4]
        list_files_with_filter(s3, regex_pattern)
    elif command == "delete-filter" and len(sys.argv) == 5:
        regex_pattern = sys.argv[4]
        delete_files_with_filter(s3, regex_pattern)
    else:
        print("Invalid command or arguments. Available commands: list, upload, list-filter, delete-filter")

if __name__ == "__main__":
    main()
