from dataclasses import dataclass, field
from typing import Dict


@dataclass
class FileMetadata:
    """
    Model representing S3 object metadata
    """

    object_key: str
    version_id: str
    content_type: str
    file_size: int
    last_modified_date: str

    metadata: Dict = field(default_factory=dict)
    tags: Dict = field(default_factory=dict)

    file_type: str = ""
    size_category: str = ""
    processing_status: str = "RECEIVED"

    def to_dict(self):
        """
        Convert object to dictionary
        """

        return {
            "object_key": self.object_key,
            "version_id": self.version_id,
            "content_type": self.content_type,
            "file_size": self.file_size,
            "last_modified_date": self.last_modified_date,
            "metadata": self.metadata,
            "tags": self.tags,
            "file_type": self.file_type,
            "size_category": self.size_category,
            "processing_status": self.processing_status
        }

    @classmethod
    def from_dict(cls, item):
        """
        Create FileMetadata object from DynamoDB item
        """

        return cls(
            object_key=item.get("object_key", ""),
            version_id=item.get("version_id", ""),
            content_type=item.get("content_type", ""),
            file_size=item.get("file_size", 0),
            last_modified_date=item.get(
                "last_modified_date",
                ""
            ),
            metadata=item.get("metadata", {}),
            tags=item.get("tags", {}),
            file_type=item.get("file_type", ""),
            size_category=item.get(
                "size_category",
                ""
            ),
            processing_status=item.get(
                "processing_status",
                "RECEIVED"
            )
        )