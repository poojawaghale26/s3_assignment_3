import os
import boto3
from botocore.exceptions import ClientError


class SNSService:
    """
    Service class for publishing messages
    to SNS Topic.
    """

    def __init__(self):
        self.sns_client = boto3.client("sns")

        self.topic_arn = os.environ.get(
            "SNS_TOPIC_ARN"
        )

        if not self.topic_arn:
            raise ValueError(
                "SNS_TOPIC_ARN environment variable is missing"
            )

    def publish_message(
        self,
        subject,
        message
    ):
        """
        Publish message to SNS Topic

        Parameters:
            subject (str): Email subject
            message (str): Message body

        Returns:
            MessageId
        """

        try:

            response = self.sns_client.publish(
                TopicArn=self.topic_arn,
                Subject=subject,
                Message=message
            )

            message_id = response["MessageId"]

            print(
                f"Message published successfully. "
                f"MessageId: {message_id}"
            )

            return message_id

        except ClientError as e:

            error_message = (
                e.response["Error"]["Message"]
            )

            print(
                f"Failed to publish SNS message: "
                f"{error_message}"
            )

            raise

    def publish_failure_alert(
        self,
        glue_job_name,
        job_run_id,
        error_message
    ):
        """
        Helper method specifically for
        Glue Job failure alerts.
        """

        subject = (
            f"Glue Job Failure Alert - "
            f"{glue_job_name}"
        )

        message = f"""
Glue Job Failed

Job Name: {glue_job_name}
Job Run ID: {job_run_id}

Error Details:
{error_message}

Please investigate the issue.
"""

        return self.publish_message(
            subject=subject,
            message=message
        )