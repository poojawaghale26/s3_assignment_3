import pytest
from unittest.mock import patch, MagicMock
import os
import sys

PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

sys.path.insert(0, PROJECT_ROOT)
from lambdas.glue_success.athena_service import AthenaService



@patch(
    "glue_success.athena_service.boto3.client"
)
def test_execute_query_success(
    mock_boto_client
):

    mock_athena = MagicMock()

    mock_boto_client.return_value = mock_athena

    mock_athena.start_query_execution.return_value = {
        "QueryExecutionId": "query-123"
    }

    mock_athena.get_query_execution.return_value = {
        "QueryExecution": {
            "Status": {
                "State": "SUCCEEDED"
            }
        }
    }

    athena_service = AthenaService()

    result = athena_service.execute_query(
        "SELECT * FROM csv_table"
    )

    assert result == "query-123"