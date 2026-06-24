import os
import boto3
from botocore.exceptions import ClientError
import os
import sys

PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        ".."
    )
)

sys.path.insert(0, PROJECT_ROOT)

from lambdas.save_s3_config.models import FileMetadata


class DynamoDBService:

    def __init__(self):
        table_name = os.environ.get(
            "DYNAMODB_TABLE",
            "FileMetadataTable"
        )

        dynamodb = boto3.resource("dynamodb")
        self.table = dynamodb.Table(table_name)

    def get_metadata(self, object_key):
        """
        Fetch file metadata from DynamoDB
        """

        try:

            response = self.table.get_item(
                Key={
                    "object_key": object_key
                }
            )

            item = response.get("Item")

            if not item:
                print(
                    f"No metadata found for "
                    f"{object_key}"
                )
                return None

            return FileMetadata.from_dict(item)

        except ClientError as e:

            print(
                f"Error fetching metadata: "
                f"{e.response['Error']['Message']}"
            )

            raise

    def update_status(
        self,
        object_key,
        status
    ):
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
                f"Updated status to "
                f"{status} for "
                f"{object_key}"
            )

        except ClientError as e:

            print(
                f"Error updating status: "
                f"{e.response['Error']['Message']}"
            )

            raise

    def mark_processing(self, object_key):
        """
        Mark file as PROCESSING
        """

        self.update_status(
            object_key,
            "PROCESSING"
        )

    def mark_completed(self, object_key):
        """
        Mark file as COMPLETED
        """

        self.update_status(
            object_key,
            "COMPLETED"
        )

    def mark_failed(self, object_key):
        """
        Mark file as FAILED
        """

        self.update_status(
            object_key,
            "FAILED"
        )

    def is_already_processed(
        self,
        object_key
    ):
        """
        Prevent duplicate processing
        """

        metadata = self.get_metadata(
            object_key
        )

        if not metadata:
            return False

        return (
            metadata.processing_status
            == "COMPLETED"
        )

    def acquire_lock(
        self,
        object_key
    ):
        """
        Prevent concurrent processing of
        same file using conditional update.

        Returns True if lock acquired.
        Returns False if already processing.
        """

        try:

            self.table.update_item(
                Key={
                    "object_key": object_key
                },
                UpdateExpression=
                "SET processing_status = :status",
                ConditionExpression=
                "processing_status <> :processing",
                ExpressionAttributeValues={
                    ":status": "PROCESSING",
                    ":processing": "PROCESSING"
                }
            )

            print(
                f"Lock acquired for "
                f"{object_key}"
            )

            return True

        except ClientError:

            print(
                f"{object_key} is already "
                f"being processed"
            )

            return False