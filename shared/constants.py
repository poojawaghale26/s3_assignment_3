"""
Common constants used across the project.
"""


# =========================
# File Types
# =========================

FILE_TYPE_CSV = "csv"
FILE_TYPE_JSON = "json"
FILE_TYPE_TEXT = "txt"


# =========================
# File Size Ranges (Bytes)
# =========================

SMALL_FILE_MAX_SIZE = 5 * 1024       # 5 KB
MEDIUM_FILE_MAX_SIZE = 10 * 1024     # 10 KB


# =========================
# Glue Job Names
# =========================

CSV_SMALL_JOB = "CSVSmallJob"
CSV_MEDIUM_JOB = "CSVMediumJob"
CSV_LARGE_JOB = "CSVLargeJob"

JSON_SMALL_JOB = "JSONSmallJob"
JSON_MEDIUM_JOB = "JSONMediumJob"
JSON_LARGE_JOB = "JSONLargeJob"

TEXT_SMALL_JOB = "TextSmallJob"
TEXT_MEDIUM_JOB = "TextMediumJob"
TEXT_LARGE_JOB = "TextLargeJob"


# =========================
# Crawlers
# =========================

CSV_CRAWLER = "CSVFilesCrawler"
JSON_CRAWLER = "JSONFilesCrawler"
TEXT_CRAWLER = "TextFilesCrawler"


# =========================
# Glue Catalog Tables
# =========================

CSV_TABLE = "csv_table"
JSON_TABLE = "json_table"
TEXT_TABLE = "text_table"


# =========================
# DynamoDB
# =========================

DYNAMODB_TABLE_NAME = "S3FileConfigTable"


# =========================
# Athena
# =========================

ATHENA_DATABASE = "file_processing_db"

CSV_VIEW = "csv_view"
JSON_VIEW = "json_view"
TEXT_VIEW = "text_view"


# =========================
# Status Values
# =========================

STATUS_PENDING = "PENDING"
STATUS_PROCESSING = "PROCESSING"
STATUS_SUCCESS = "SUCCESS"
STATUS_FAILED = "FAILED"


# =========================
# Glue States
# =========================

GLUE_STATE_SUCCEEDED = "SUCCEEDED"
GLUE_STATE_FAILED = "FAILED"
GLUE_STATE_RUNNING = "RUNNING"


# =========================
# Crawler States
# =========================

CRAWLER_READY = "READY"
CRAWLER_RUNNING = "RUNNING"
CRAWLER_STOPPING = "STOPPING"


# =========================
# Athena Query States
# =========================

ATHENA_QUERY_RUNNING = "RUNNING"
ATHENA_QUERY_SUCCEEDED = "SUCCEEDED"
ATHENA_QUERY_FAILED = "FAILED"
ATHENA_QUERY_CANCELLED = "CANCELLED"


# =========================
# Country Mapping
# =========================

COUNTRY_CODE_MAPPING = {
    "India": "IN",
    "United States": "US",
    "Canada": "CA",
    "Australia": "AU",
    "Germany": "DE",
    "France": "FR",
    "Japan": "JP",
    "China": "CN"
}


# =========================
# Retry Configuration
# =========================

MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 5

CRAWLER_WAIT_TIMEOUT_MINUTES = 5
ATHENA_WAIT_TIMEOUT_SECONDS = 300