"""
Video URL service for Google Drive integration.

This module provides a service to convert video IDs from the VSL database
to embeddable Google Drive URLs.
"""

import json
from pathlib import Path
from typing import Optional


class VideoService:
    """
    Service for managing video URL mappings.

    This class follows the Singleton pattern to ensure video mappings
    are loaded only once and reused throughout the application lifecycle.
    """

    _instance: Optional["VideoService"] = None
    _initialized: bool = False

    def __new__(cls, mapping_path: Optional[str] = None) -> "VideoService":
        """Ensure only one instance exists."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, mapping_path: Optional[str] = None):
        """
        Initialize the VideoService.

        Args:
            mapping_path: Path to the video mapping JSON file
        """
        # Skip if already initialized
        if VideoService._initialized:
            return

        # Set default mapping path
        if mapping_path is None:
            project_root = Path(__file__).parent.parent.parent
            mapping_path = str(project_root / "data" / "video_mapping.json")

        self.mapping_path = Path(mapping_path)
        self._mapping: dict[str, str] = {}
        self._load_mapping()

        VideoService._initialized = True

    def _load_mapping(self) -> None:
        """
        Load video ID to Google Drive file ID mapping from JSON file.

        If the mapping file doesn't exist, an empty mapping is used.
        """
        if self.mapping_path.exists():
            try:
                with open(self.mapping_path, "r", encoding="utf-8") as f:
                    self._mapping = json.load(f)
                print(f"Loaded {len(self._mapping)} video mappings from {self.mapping_path}")
            except Exception as e:
                print(f"Warning: Failed to load video mapping: {e}")
                self._mapping = {}
        else:
            print(f"Warning: Video mapping file not found: {self.mapping_path}")
            self._mapping = {}

    def get_video_url(self, video_id: str) -> Optional[str]:
        if not video_id:
            return None

        file_id = self._mapping.get(video_id)
        if file_id:
            return f"https://drive.google.com/file/d/{file_id}/view?usp=drive_link"
        return None

    def get_download_url(self, video_id: str) -> Optional[str]:
        """
        Get direct download URL for a video ID.

        Args:
            video_id: Video ID from VSL_DATA

        Returns:
            Direct download Google Drive URL or None if not found
        """
        if not video_id:
            return None

        file_id = self._mapping.get(video_id)
        if file_id:
            return f"https://drive.google.com/uc?export=download&id={file_id}"
        return None

    def get_view_url(self, video_id: str) -> Optional[str]:
        """
        Get standard Google Drive view URL for a video ID.

        Args:
            video_id: Video ID from VSL_DATA

        Returns:
            Standard Google Drive view URL or None if not found
        """
        if not video_id:
            return None

        file_id = self._mapping.get(video_id)
        if file_id:
            return f"https://drive.google.com/file/d/{file_id}/view"
        return None

    def has_video(self, video_id: str) -> bool:
        """
        Check if a video ID has a mapping.

        Args:
            video_id: Video ID to check

        Returns:
            True if mapping exists, False otherwise
        """
        if not video_id:
            return False
        return video_id in self._mapping

    def get_all_video_ids(self) -> list[str]:
        """
        Get all available video IDs.

        Returns:
            List of all video IDs that have mappings
        """
        return list(self._mapping.keys())

    def get_mapping_count(self) -> int:
        """
        Get the total number of video mappings.

        Returns:
            Number of video mappings loaded
        """
        return len(self._mapping)

    def reload_mapping(self) -> None:
        """
        Reload the video mapping from file.

        Use this if the mapping file has been updated and you want to
        refresh the mappings without restarting the application.
        """
        self._mapping = {}
        self._load_mapping()

    @classmethod
    def reset(cls) -> None:
        """
        Reset the singleton instance.

        Use this to force re-initialization, for example in testing
        or when the mapping file path changes.
        """
        cls._instance = None
        cls._initialized = False

    def __repr__(self) -> str:
        """String representation of the VideoService."""
        return f"VideoService(mappings={len(self._mapping)}, path={self.mapping_path})"


# Global singleton instance
_video_service_instance: Optional[VideoService] = None


def get_video_service(mapping_path: Optional[str] = None) -> VideoService:
    """
    Get the singleton VideoService instance.

    Args:
        mapping_path: Optional path to video mapping file

    Returns:
        VideoService singleton instance

    Example:
        >>> from backend.core.video_service import get_video_service
        >>> service = get_video_service()
        >>> url = service.get_video_url("D0001B")
    """
    global _video_service_instance
    if _video_service_instance is None:
        _video_service_instance = VideoService(mapping_path)
    return _video_service_instance
