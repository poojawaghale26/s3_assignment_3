import json
import boto3
import os
from datetime import datetime

# AWS Clients
s3_client = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")

# Environment Variable
TABLE_NAME = os.environ.get("DYNAMODB_TABLE", "FileMetadataTable")

table = dynamodb.Table(TABLE_NAME)


class S3MetadataService:

    @staticmethod
    def get_object_details(bucket_name, object_key):

        # Get object metadata
        response = s3_client.head_object(
            Bucket=bucket_name,
            Key=object_key
        )

        # Get object tags
        try:
            tag_response = s3_client.get_object_tagging(
                Bucket=bucket_name,
                Key=object_key
            )

            tags = {
                tag["Key"]: tag["Value"]
                for tag in tag_response["TagSet"]
            }

        except Exception:
            tags = {}

        return {
            "object_key": object_key,
            "version_id": response.get("VersionId", "N/A"),
            "content_type": response.get("ContentType", ""),
            "file_size": response.get("ContentLength", 0),
            "last_modified_date": response["LastModified"].isoformat(),
            "metadata": response.get("Metadata", {}),
            "tags": tags
        }


class DynamoDBService:

    @staticmethod
    def save_metadata(item):

        table.put_item(Item=item)


def lambda_handler(event, context):

    try:

        print("Received Event:")
        print(json.dumps(event))

        for record in event["Records"]:

            # SNS Message
            sns_message = json.loads(record["Sns"]["Message"])

            # S3 Event Record
            s3_record = sns_message["Records"][0]

            bucket_name = s3_record["s3"]["bucket"]["name"]
            object_key = s3_record["s3"]["object"]["key"]

            print(f"Processing file: {object_key}")

            metadata = S3MetadataService.get_object_details(
                bucket_name,
                object_key
            )

            DynamoDBService.save_metadata(metadata)

            print(
                f"Metadata saved successfully for {object_key}"
            )

        return {
            "statusCode": 200,
            "body": json.dumps(
                "Metadata stored successfully"
            )
        }

    except Exception as e:

        print(f"Error: {str(e)}")

        return {
            "statusCode": 500,
            "body": json.dumps(str(e))
        }