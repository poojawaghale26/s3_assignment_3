import boto3
from botocore.exceptions import ClientError


class GlueService:

    def __init__(self):
        self.glue_client = boto3.client("glue")

    def start_job(self, job_name, object_key):
        """
        Start a Glue Job and return JobRunId
        """

        try:

            response = self.glue_client.start_job_run(
                JobName=job_name,
                Arguments={
                    "--object_key": object_key
                }
            )

            job_run_id = response["JobRunId"]

            print(
                f"Started Glue Job: {job_name}, "
                f"JobRunId: {job_run_id}"
            )

            return job_run_id

        except ClientError as e:

            print(
                f"Failed to start Glue Job "
                f"{job_name}: "
                f"{e.response['Error']['Message']}"
            )

            raise

    def get_job_status(self, job_name, job_run_id):
        """
        Get Glue Job status
        """

        try:

            response = self.glue_client.get_job_run(
                JobName=job_name,
                RunId=job_run_id
            )

            return response["JobRun"]["JobRunState"]

        except ClientError as e:

            print(
                f"Unable to fetch job status: "
                f"{e.response['Error']['Message']}"
            )

            raise

    def stop_job(self, job_name, job_run_id):
        """
        Stop a running Glue Job
        """

        try:

            response = self.glue_client.batch_stop_job_run(
                JobName=job_name,
                JobRunIds=[job_run_id]
            )

            print(
                f"Stopped Job: {job_name}"
            )

            return response

        except ClientError as e:

            print(
                f"Unable to stop job: "
                f"{e.response['Error']['Message']}"
            )

            raise