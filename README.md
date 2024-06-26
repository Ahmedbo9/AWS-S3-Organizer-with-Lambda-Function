# AWS S3 Organizer with Lambda Function

## Project Summary

This project demonstrates how to use Python and AWS Lambda Functions to automate the organization of files in an S3 bucket. The Lambda function triggers when a file is added to an S3 bucket and moves it to a folder structured as `YYYYMMDD/filename`, based on the file's creation date.

## Table of Contents

- [Prerequisites](#prerequisites)
- [AWS Services Used](#aws-services-used)
- [Project Setup](#project-setup)
- [Deployment](#deployment)
- [Usage](#usage)
- [Code](#code)

## Prerequisites

Before you begin, ensure you have the following:

- An AWS account
- Basic knowledge of Python and AWS Lambda
- AWS CLI installed and configured on your local machine
- Necessary IAM permissions to create and manage Lambda functions, S3 buckets, and IAM roles

## AWS Services Used

- **AWS Lambda:** Used to create the function that handles the file moving logic.
- **Amazon S3:** Used to store the files and trigger the Lambda function upon file upload.
- **IAM Role:** Used to grant the necessary permissions for the Lambda function to interact with the S3 bucket.

## Project Setup

1. **Create the IAM Role:**

    Create an IAM role with the necessary permissions for the Lambda function to interact with S3. Attach the following policies:
    
    - `AWSLambdaBasicExecutionRole`
    - `AmazonS3FullAccess`

2. **Set Up the Environment:**

    Make sure you have configured your AWS CLI with the necessary credentials and region.

    ```bash
    aws configure
    ```

## Deployment

1. **Create an S3 Bucket:**

    Log in to the AWS Management Console and create an S3 bucket. Note the bucket name for use in the Lambda function configuration.

2. **Create the Lambda Function:**

    - Log in to the AWS Management Console.
    - Navigate to AWS Lambda.
    - Create a new Lambda function.
    - Choose Python as the runtime.
    - Assign the previously created IAM role to the Lambda function.
    - Upload the `migration_script.py` code.
    - Set up the S3 bucket as the trigger for the Lambda function.

## Usage

Once deployed, the Lambda function will automatically trigger whenever a new file is uploaded to the specified S3 bucket. It will then move the file to a folder structured as `YYYYMMDD/filename`, based on the file's creation date.

## Code

Here's the `migration_script.py` code used in this project:

```python
import boto3
from datetime import datetime

today = datetime.today().strftime('%Y-%m-%d')

def lambda_handler(event, context):
    client = boto3.client('s3')
    bucket_name = 'abo-s3-organizer'

    list_of_objects = client.list_objects_v2(Bucket=bucket_name)

    s3_bucket_contents = list_of_objects['Contents']

    object_name_and_folder_list = []

    for item in s3_bucket_contents:
        object_name = item['Key']
        object_name_and_folder_list.append(object_name)

    directory_name = today + '/'

    if directory_name in object_name_and_folder_list:
        print('Directory already exists')
    else:
        print('Directory does not exist, adding new folder')
        client.put_object(Bucket=bucket_name, Key=directory_name)

    for item in s3_bucket_contents:
        creation_date = item['LastModified'].strftime('%Y-%m-%d') + '/'
        object_name = item['Key']

        if creation_date == directory_name and '/' not in object_name:
            print('Moving object: ' + object_name + ' to ' + directory_name)
            copy_source = bucket_name + '/' + object_name
            client.copy_object(
                Bucket=bucket_name, CopySource=copy_source, Key=directory_name + object_name)
            print('Deleting object from:' + bucket_name)
            client.delete_object(Bucket=bucket_name, Key=object_name)
