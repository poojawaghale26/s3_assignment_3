import boto3
import time
from botocore.exceptions import ClientError


class CrawlerService:

    def __init__(self):
        self.glue_client = boto3.client("glue")

    def start_crawler(self, crawler_name):
        """
        Start the specified crawler.
        """

        try:

            crawler = self.glue_client.get_crawler(
                Name=crawler_name
            )

            crawler_state = crawler["Crawler"]["State"]

            if crawler_state == "RUNNING":

                print(
                    f"Crawler {crawler_name} "
                    f"is already running"
                )

                return

            self.glue_client.start_crawler(
                Name=crawler_name
            )

            print(
                f"Crawler started: "
                f"{crawler_name}"
            )

        except ClientError as e:

            print(
                f"Error starting crawler "
                f"{crawler_name}: "
                f"{e.response['Error']['Message']}"
            )

            raise

    def get_crawler_state(self, crawler_name):
        """
        Get current crawler state.
        """

        try:

            response = self.glue_client.get_crawler(
                Name=crawler_name
            )

            return response["Crawler"]["State"]

        except ClientError as e:

            print(
                f"Error fetching crawler state: "
                f"{e.response['Error']['Message']}"
            )

            raise

    def wait_for_completion(
        self,
        crawler_name,
        timeout_minutes=5
    ):
        """
        Wait until crawler completes.

        Poll every 30 seconds.
        Timeout after specified minutes.
        """

        timeout_seconds = (
            timeout_minutes * 60
        )

        polling_interval = 30

        elapsed_time = 0

        while elapsed_time < timeout_seconds:

            state = self.get_crawler_state(
                crawler_name
            )

            print(
                f"Crawler State: {state}"
            )

            if state == "READY":

                print(
                    f"Crawler completed: "
                    f"{crawler_name}"
                )

                return True

            time.sleep(
                polling_interval
            )

            elapsed_time += (
                polling_interval
            )

        raise TimeoutError(
            f"Crawler {crawler_name} "
            f"did not complete within "
            f"{timeout_minutes} minutes"
        )