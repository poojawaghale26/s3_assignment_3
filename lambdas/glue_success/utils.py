import time


class GlueJobMapper:
    """
    Maps Glue Jobs to Crawlers and Tables
    """

    CRAWLER_MAPPING = {
        "CSVSmallJob": "CSVFilesCrawler",
        "CSVMediumJob": "CSVFilesCrawler",
        "CSVLargeJob": "CSVFilesCrawler",

        "JSONSmallJob": "JSONFilesCrawler",
        "JSONMediumJob": "JSONFilesCrawler",
        "JSONLargeJob": "JSONFilesCrawler",

        "TextSmallJob": "TextFilesCrawler",
        "TextMediumJob": "TextFilesCrawler",
        "TextLargeJob": "TextFilesCrawler"
    }

    TABLE_MAPPING = {
        "CSVSmallJob": "csv_table",
        "CSVMediumJob": "csv_table",
        "CSVLargeJob": "csv_table",

        "JSONSmallJob": "json_table",
        "JSONMediumJob": "json_table",
        "JSONLargeJob": "json_table",

        "TextSmallJob": "text_table",
        "TextMediumJob": "text_table",
        "TextLargeJob": "text_table"
    }

    @classmethod
    def get_crawler_name(cls, glue_job_name):

        crawler_name = cls.CRAWLER_MAPPING.get(
            glue_job_name
        )

        if not crawler_name:
            raise ValueError(
                f"No crawler found for "
                f"{glue_job_name}"
            )

        return crawler_name

    @classmethod
    def get_table_name(cls, glue_job_name):

        table_name = cls.TABLE_MAPPING.get(
            glue_job_name
        )

        if not table_name:
            raise ValueError(
                f"No table found for "
                f"{glue_job_name}"
            )

        return table_name


class AthenaQueryBuilder:
    """
    Builds Athena queries
    """

    @staticmethod
    def select_all_query(table_name):

        return f"""
        SELECT *
        FROM {table_name}
        """

    @staticmethod
    def create_view_query(
        table_name,
        view_name
    ):

        return f"""
        CREATE OR REPLACE VIEW {view_name} AS
        SELECT
            name,
            age,
            country,
            country_code
        FROM {table_name}
        """


class RetryHelper:
    """
    Generic retry helper
    """

    @staticmethod
    def retry(
        function,
        retries=3,
        delay=5,
        *args,
        **kwargs
    ):

        for attempt in range(retries):

            try:
                return function(
                    *args,
                    **kwargs
                )

            except Exception as e:

                print(
                    f"Attempt "
                    f"{attempt + 1} failed: {e}"
                )

                if attempt < retries - 1:
                    time.sleep(delay)

        raise Exception(
            f"Function failed after "
            f"{retries} retries"
        )