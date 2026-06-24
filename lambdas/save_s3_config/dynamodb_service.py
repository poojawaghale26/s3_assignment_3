import boto3
import os
from botocore.exceptions import ClientError


class DynamoDBService:

    def __init__(self):
        table_name = os.environ.get(
            "DYNAMODB_TABLE",
            "FileMetadataTable"
        )

        dynamodb = boto3.resource("dynamodb")
        self.table = dynamodb.Table(table_name)

    def save_metadata(self, metadata):
        """
        Save file metadata to DynamoDB
        """

        try:
            self.table.put_item(Item=metadata)

            print(
                f"Metadata saved successfully for "
                f"{metadata['object_key']}"
            )

            return True

        except ClientError as e:

            print(
                f"Error saving metadata: "
                f"{e.response['Error']['Message']}"
            )

            raise

    def get_metadata(self, object_key):
        """
        Retrieve metadata from DynamoDB
        """

        try:
            response = self.table.get_item(
                Key={
                    "object_key": object_key
                }
            )

            return response.get("Item")

        except ClientError as e:

            print(
                f"Error retrieving metadata: "
                f"{e.response['Error']['Message']}"
            )

            raise

    def update_status(self, object_key, status):
        """
        Update processing status
        """

        try:
            self.table.update_item(
                Key={
                    "object_key": object_key
                },
                UpdateExpression=
                "SET processing_status = :status",
                ExpressionAttributeValues={
                    ":status": status
                }
            )

            print(
                f"Status updated to {status} "
                f"for {object_key}"
            )

        except ClientError as e:

            print(
                f"Error updating status: "
                f"{e.response['Error']['Message']}"
            )

            raise

    def is_already_processed(self, object_key):
        """
        Check if file has already been processed
        (helps prevent duplicate processing)
        """

        item = self.get_metadata(object_key)

        if not item:
            return False

        return item.get("processing_status") == "COMPLETED"