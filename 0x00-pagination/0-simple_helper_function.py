#!/usr/bin/env python3
"""
This is a simple helper process.
"""
from typing import Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """
    Fetches an index range in a page with page size.
    """
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    return start_index, end_index
