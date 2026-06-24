import json

from dynamodb_service import DynamoDBService
from glue_service import GlueService
from job_selector import JobSelector


dynamodb_service = DynamoDBService()
glue_service = GlueService()
job_selector = JobSelector()


def lambda_handler(event, context):
    """
    Lambda triggered by SNS when a file lands in S3.
    Reads metadata from DynamoDB and starts
    the appropriate Glue Job.
    """

    try:

        print("Received Event:")
        print(json.dumps(event))

        for record in event["Records"]:

            # SNS Message
            sns_message = json.loads(
                record["Sns"]["Message"]
            )

            # Original S3 Event
            s3_record = sns_message["Records"][0]

            object_key = (
                s3_record["s3"]["object"]["key"]
            )

            print(
                f"Processing file: {object_key}"
            )

            # Get metadata from DynamoDB
            metadata = (
                dynamodb_service.get_metadata(
                    object_key
                )
            )

            if not metadata:
                raise Exception(
                    f"No metadata found for "
                    f"{object_key}"
                )

            # Prevent duplicate processing
            if (
                metadata.processing_status
                == "COMPLETED"
            ):
                print(
                    f"{object_key} already processed"
                )
                continue

            # Select Glue Job
            glue_job_name = (
                job_selector.select_job(
                    metadata.file_type,
                    metadata.file_size
                )
            )

            print(
                f"Selected Glue Job: "
                f"{glue_job_name}"
            )

            # Update status
            dynamodb_service.update_status(
                object_key,
                "PROCESSING"
            )

            # Start Glue Job
            job_run_id = (
                glue_service.start_job(
                    glue_job_name,
                    object_key
                )
            )

            print(
                f"Glue Job Started: "
                f"{job_run_id}"
            )

        return {
            "statusCode": 200,
            "body": json.dumps(
                "Glue job started successfully"
            )
        }

    except Exception as e:

        print(f"Error: {str(e)}")

        return {
            "statusCode": 500,
            "body": json.dumps(str(e))
        }