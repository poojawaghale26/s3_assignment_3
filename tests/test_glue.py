import os
import sys
import pytest
PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

sys.path.insert(0, PROJECT_ROOT)


from lambdas.run_glue_job.job_selector import JobSelector


class TestJobSelector:

    def setup_method(self):
        self.selector = JobSelector()

    # CSV Tests

    def test_csv_small_job(self):

        job_name = self.selector.select_job(
            file_type="csv",
            file_size=3000
        )

        assert job_name == "CSVSmallJob"

    def test_csv_medium_job(self):

        job_name = self.selector.select_job(
            file_type="csv",
            file_size=7000
        )

        assert job_name == "CSVMediumJob"

    def test_csv_large_job(self):

        job_name = self.selector.select_job(
            file_type="csv",
            file_size=15000
        )

        assert job_name == "CSVLargeJob"

    # JSON Tests

    def test_json_small_job(self):

        job_name = self.selector.select_job(
            file_type="json",
            file_size=4000
        )

        assert job_name == "JSONSmallJob"

    def test_json_medium_job(self):

        job_name = self.selector.select_job(
            file_type="json",
            file_size=8000
        )

        assert job_name == "JSONMediumJob"

    def test_json_large_job(self):

        job_name = self.selector.select_job(
            file_type="json",
            file_size=20000
        )

        assert job_name == "JSONLargeJob"

    # Text Tests

    def test_text_small_job(self):

        job_name = self.selector.select_job(
            file_type="txt",
            file_size=2000
        )

        assert job_name == "TextSmallJob"

    def test_text_medium_job(self):

        job_name = self.selector.select_job(
            file_type="txt",
            file_size=6000
        )

        assert job_name == "TextMediumJob"

    def test_text_large_job(self):

        job_name = self.selector.select_job(
            file_type="txt",
            file_size=12000
        )

        assert job_name == "TextLargeJob"

    # Negative Test

    def test_invalid_file_type(self):

        with pytest.raises(Exception):

            self.selector.select_job(
                file_type="pdf",
                file_size=1000
            )