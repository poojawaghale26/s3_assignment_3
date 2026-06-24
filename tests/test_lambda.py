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

from lambdas.glue_success.athena_service import AthenaService


class TestAthenaService:

    @patch("glue_success.athena_service.boto3.client")
    def test_execute_query_success(
        self,
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

        query_id = athena_service.execute_query(
            "SELECT * FROM csv_table"
        )

        assert query_id == "query-123"

        mock_athena.start_query_execution.assert_called_once()

    @patch("glue_success.athena_service.boto3.client")
    def test_query_failed(
        self,
        mock_boto_client
    ):

        mock_athena = MagicMock()

        mock_boto_client.return_value = mock_athena

        mock_athena.start_query_execution.return_value = {
            "QueryExecutionId": "query-456"
        }

        mock_athena.get_query_execution.return_value = {
            "QueryExecution": {
                "Status": {
                    "State": "FAILED",
                    "StateChangeReason":
                    "Syntax Error"
                }
            }
        }

        athena_service = AthenaService()

        try:

            athena_service.execute_query(
                "INVALID QUERY"
            )

            assert False

        except Exception as e:

            assert "Syntax Error" in str(e)

    @patch("glue_success.athena_service.boto3.client")
    def test_get_query_results(
        self,
        mock_boto_client
    ):

        mock_athena = MagicMock()

        mock_boto_client.return_value = mock_athena

        expected_response = {
            "ResultSet": {
                "Rows": [
                    {
                        "Data": [
                            {
                                "VarCharValue":
                                "Pooja"
                            }
                        ]
                    }
                ]
            }
        }

        mock_athena.get_query_results.return_value = (
            expected_response
        )

        athena_service = AthenaService()

        result = (
            athena_service.get_query_results(
                "query-123"
            )
        )

        assert result == expected_response