import json

from crawler_service import CrawlerService
from athena_service import AthenaService


crawler_service = CrawlerService()
athena_service = AthenaService()


def lambda_handler(event, context):
    """
    Triggered by EventBridge when a Glue Job
    completes successfully.
    """

    try:

        print("Received Event:")
        print(json.dumps(event))

        # Glue Job Name from EventBridge Event
        glue_job_name = event["detail"]["jobName"]

        print(
            f"Glue Job Succeeded: "
            f"{glue_job_name}"
        )

        # Determine crawler and table
        crawler_name = get_crawler_name(
            glue_job_name
        )

        table_name = get_table_name(
            glue_job_name
        )

        print(
            f"Starting crawler: "
            f"{crawler_name}"
        )

        # Start crawler
        crawler_service.start_crawler(
            crawler_name
        )

        # Wait until crawler completes
        crawler_service.wait_for_completion(
            crawler_name,
            timeout_minutes=5
        )

        print(
            f"Crawler completed: "
            f"{crawler_name}"
        )

        # Execute Athena Query
        query = (
            f"SELECT * FROM "
            f"{table_name}"
        )

        query_execution_id = (
            athena_service.execute_query(
                query
            )
        )

        print(
            f"Athena Query Started: "
            f"{query_execution_id}"
        )

        return {
            "statusCode": 200,
            "body": json.dumps(
                "Crawler and Athena query executed"
            )
        }

    except Exception as e:

        print(f"Error: {str(e)}")

        return {
            "statusCode": 500,
            "body": json.dumps(str(e))
        }


def get_crawler_name(glue_job_name):
    """
    Map Glue Job to Crawler
    """

    if glue_job_name.startswith("CSV"):
        return "CSVFilesCrawler"

    elif glue_job_name.startswith("JSON"):
        return "JSONFilesCrawler"

    elif glue_job_name.startswith("Text"):
        return "TextFilesCrawler"

    raise Exception(
        f"No crawler mapping found for "
        f"{glue_job_name}"
    )


def get_table_name(glue_job_name):
    """
    Map Glue Job to Glue Catalog Table
    """

    if glue_job_name.startswith("CSV"):
        return "csv_table"

    elif glue_job_name.startswith("JSON"):
        return "json_table"

    elif glue_job_name.startswith("Text"):
        return "text_table"

    raise Exception(
        f"No table mapping found for "
        f"{glue_job_name}"
    )