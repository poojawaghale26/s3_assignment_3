import os
import time
import boto3
from botocore.exceptions import ClientError


class AthenaService:

    def __init__(self):
        self.athena_client = boto3.client("athena")

        self.database = os.environ.get(
            "GLUE_DATABASE",
            "file_processing_db"
        )

        self.output_location = os.environ.get(
            "ATHENA_OUTPUT_LOCATION",
            "s3://athena-output-demo/results/"
        )

    def execute_query(self, query):
        """
        Execute Athena query and return QueryExecutionId
        """

        try:

            response = self.athena_client.start_query_execution(
                QueryString=query,
                QueryExecutionContext={
                    "Database": self.database
                },
                ResultConfiguration={
                    "OutputLocation": self.output_location
                }
            )

            query_execution_id = response[
                "QueryExecutionId"
            ]

            print(
                f"Athena Query Started: "
                f"{query_execution_id}"
            )

            self.wait_for_completion(
                query_execution_id
            )

            return query_execution_id

        except ClientError as e:

            print(
                f"Error executing Athena query: "
                f"{e.response['Error']['Message']}"
            )

            raise

    def wait_for_completion(
        self,
        query_execution_id,
        timeout_seconds=300
    ):
        """
        Wait until Athena query completes.
        Maximum wait time = 5 minutes
        """

        elapsed_time = 0
        polling_interval = 5

        while elapsed_time < timeout_seconds:

            response = (
                self.athena_client.get_query_execution(
                    QueryExecutionId=query_execution_id
                )
            )

            state = response[
                "QueryExecution"
            ]["Status"]["State"]

            print(
                f"Query Status: {state}"
            )

            if state == "SUCCEEDED":

                print(
                    f"Query completed successfully"
                )

                return True

            if state in [
                "FAILED",
                "CANCELLED"
            ]:

                reason = response[
                    "QueryExecution"
                ]["Status"].get(
                    "StateChangeReason",
                    "Unknown Error"
                )

                raise Exception(
                    f"Athena query failed: "
                    f"{reason}"
                )

            time.sleep(
                polling_interval
            )

            elapsed_time += (
                polling_interval
            )

        raise TimeoutError(
            "Athena query timed out"
        )

    def get_query_results(
        self,
        query_execution_id
    ):
        """
        Fetch Athena query results.
        """

        try:

            response = (
                self.athena_client.get_query_results(
                    QueryExecutionId=query_execution_id
                )
            )

            return response

        except ClientError as e:

            print(
                f"Error fetching query results: "
                f"{e.response['Error']['Message']}"
            )

            raise