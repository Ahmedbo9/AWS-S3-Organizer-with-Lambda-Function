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
        print('Directory does not exist , adding new folder')
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
