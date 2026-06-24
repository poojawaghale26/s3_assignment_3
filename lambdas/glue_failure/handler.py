import json
from sns_service import SNSService


sns_service = SNSService()


def lambda_handler(event, context):
    """
    Triggered by EventBridge when a Glue Job fails.
    Sends failure notification through SNS.
    """

    try:

        print("Received Event:")
        print(json.dumps(event))

        # Extract details from EventBridge event
        detail = event.get("detail", {})

        glue_job_name = detail.get(
            "jobName",
            "Unknown Job"
        )

        job_run_id = detail.get(
            "jobRunId",
            "Unknown RunId"
        )

        state = detail.get(
            "state",
            "FAILED"
        )

        error_message = detail.get(
            "message",
            "No error message available"
        )

        subject = (
            f"Glue Job Failure Alert - "
            f"{glue_job_name}"
        )

        message = f"""
Glue Job Failed

Job Name: {glue_job_name}
Job Run ID: {job_run_id}
State: {state}

Error Details:
{error_message}

Please investigate the issue.
"""

        # Publish to SNS Topic
        sns_service.publish_message(
            subject=subject,
            message=message
        )

        print(
            f"Failure notification sent for "
            f"{glue_job_name}"
        )

        return {
            "statusCode": 200,
            "body": json.dumps(
                "Failure notification sent"
            )
        }

    except Exception as e:

        print(
            f"Error sending notification: "
            f"{str(e)}"
        )

        return {
            "statusCode": 500,
            "body": json.dumps(str(e))
        }