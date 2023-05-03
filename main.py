import os
import subprocess
from dotenv import load_dotenv
import boto3
from botocore.exceptions import ClientError
import pathlib
import logging
import shutil


load_dotenv()

REGION = os.getenv('REGION')
DOMAIN = os.getenv('DOMAIN')
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
BUCKET_NAME = os.getenv('BUCKET_NAME')

output_folder = '/tmp/output'

output_path = pathlib.Path(output_folder)
if output_path.exists():
    shutil.rmtree(output_path)
else:
    output_path.mkdir(parents=True, exist_ok=True)
    
# Run the command in synchronous manner
command = f"metadata_collector collect_data -r {REGION} -d {DOMAIN} -c -b -u {USERNAME} -p {PASSWORD} -o {output_folder}"
#print(command)
response = subprocess.run(command.split(), capture_output=True, text=True)
result = response.stdout.strip("\n")
print(result)


def upload_file_to_s3(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
        print(response)
    except ClientError as e:
        logging.error(e)
        return False
    return True
    

# Upload file to S3 bucket
file_name = f'{output_folder}.zip'
upload_file_to_s3(file_name, bucket=BUCKET_NAME, object_name=None)

