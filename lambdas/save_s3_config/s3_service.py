import boto3
from botocore.exceptions import ClientError


class S3MetadataService:

    def __init__(self):
        self.s3_client = boto3.client("s3")

    def get_object_details(self, bucket_name, object_key):
        """
        Fetch S3 object metadata and tags
        """

        try:
            response = self.s3_client.head_object(
                Bucket=bucket_name,
                Key=object_key
            )

            tags = self.get_object_tags(
                bucket_name,
                object_key
            )

            metadata = {
                "object_key": object_key,
                "version_id": response.get(
                    "VersionId",
                    "N/A"
                ),
                "content_type": response.get(
                    "ContentType",
                    "unknown"
                ),
                "file_size": response.get(
                    "ContentLength",
                    0
                ),
                "last_modified_date": response[
                    "LastModified"
                ].isoformat(),
                "metadata": response.get(
                    "Metadata",
                    {}
                ),
                "tags": tags,
                "processing_status": "RECEIVED"
            }

            return metadata

        except ClientError as e:
            print(
                f"Error fetching metadata for "
                f"{object_key}: "
                f"{e.response['Error']['Message']}"
            )
            raise

    def get_object_tags(self, bucket_name, object_key):
        """
        Fetch object tags
        """

        try:

            response = self.s3_client.get_object_tagging(
                Bucket=bucket_name,
                Key=object_key
            )

            return {
                tag["Key"]: tag["Value"]
                for tag in response["TagSet"]
            }

        except ClientError:
            return {}

    def get_file_extension(self, object_key):
        """
        Extract file extension
        """

        if "." not in object_key:
            return "unknown"

        return object_key.split(".")[-1].lower()

    def get_file_size_category(self, file_size):
        """
        Determine file size category
        """

        if file_size <= 5 * 1024:
            return "SMALL"

        elif file_size <= 10 * 1024:
            return "MEDIUM"

        return "LARGE"