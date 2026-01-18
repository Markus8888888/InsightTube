# -----------------------------
# Data storage / normalization / search
# -----------------------------

from __future__ import annotations

import os
import re
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional
from urllib.parse import parse_qs, urlparse

import requests

class YouTubeDataProcessor:
    """
    Responsible for:
      - storing records (from frontend or from YouTubeLinkProcessor)
      - normalization helpers
      - searching (comments primary, title secondary)
    """

    def __init__(self, initial_data: Optional[List[Dict[str, Any]]] = None):
        self._data: List[Dict[str, Any]] = []
        if initial_data is not None:
            self.set_data(initial_data)

    def set_data(self, data: List[Dict[str, Any]]) -> None:
        if not isinstance(data, list):
            raise TypeError("Data must be a list of video dictionaries.")
        for i, item in enumerate(data):
            if not isinstance(item, dict):
                raise TypeError(f"Video at index {i} is not a dict.")
        self._data = data

    def extend_data(self, data: List[Dict[str, Any]]) -> None:
        if not isinstance(data, list):
            raise TypeError("Data must be a list of video dictionaries.")
        for i, item in enumerate(data):
            if not isinstance(item, dict):
                raise TypeError(f"Video at index {i} is not a dict.")
        self._data.extend(data)

    def add_record(self, record: Dict[str, Any]) -> None:
        if not isinstance(record, dict):
            raise TypeError("Record must be a dict.")
        self._data.append(record)

    def _normalize_text(self, value: Any) -> str:
        if value is None:
            return ""
        return str(value).strip().lower()

    def _normalize_comments(self, comments: Any) -> List[str]:
        if comments is None:
            return []
        if isinstance(comments, str):
            comments_list: Iterable[Any] = [comments]
        elif isinstance(comments, (list, tuple)):
            comments_list = comments
        else:
            return []

        out: List[str] = []
        for c in comments_list:
            txt = self._normalize_text(c)
            if txt:
                out.append(txt)
        return out

    def search_videos(self, query: str, data: Optional[List[Dict[str, Any]]] = None) -> List[Dict[str, Any]]:
        q = self._normalize_text(query)
        if not q:
            return []

        dataset = data if data is not None else self._data
        if not dataset:
            return []

        results: List[Dict[str, Any]] = []
        for video in dataset:
            title = self._normalize_text(video.get("title", ""))
            comments = self._normalize_comments(video.get("comments"))
            if any(q in c for c in comments) or (q in title):
                results.append(video)

        return results