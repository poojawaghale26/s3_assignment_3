class JobSelector:
    """
    Selects the appropriate Glue Job based on
    file type and file size.
    """

    SMALL_FILE_SIZE = 5 * 1024      # 5 KB
    MEDIUM_FILE_SIZE = 10 * 1024    # 10 KB

    JOB_MAPPING = {
        "csv": {
            "small": "CSVSmallJob",
            "medium": "CSVMediumJob",
            "large": "CSVLargeJob"
        },
        "json": {
            "small": "JSONSmallJob",
            "medium": "JSONMediumJob",
            "large": "JSONLargeJob"
        },
        "txt": {
            "small": "TextSmallJob",
            "medium": "TextMediumJob",
            "large": "TextLargeJob"
        },
        "text": {
            "small": "TextSmallJob",
            "medium": "TextMediumJob",
            "large": "TextLargeJob"
        }
    }

    def select_job(self, file_type, file_size):
        """
        Returns Glue Job Name based on
        file type and file size.

        Parameters:
            file_type (str): csv, json, txt
            file_size (int): size in bytes

        Returns:
            str: Glue Job Name
        """

        file_type = file_type.lower()

        if file_type not in self.JOB_MAPPING:
            raise ValueError(
                f"Unsupported file type: {file_type}"
            )

        if file_size <= self.SMALL_FILE_SIZE:
            size_category = "small"

        elif file_size <= self.MEDIUM_FILE_SIZE:
            size_category = "medium"

        else:
            size_category = "large"

        job_name = self.JOB_MAPPING[file_type][size_category]

        print(
            f"File Type: {file_type}, "
            f"File Size: {file_size} bytes, "
            f"Selected Job: {job_name}"
        )

        return job_name