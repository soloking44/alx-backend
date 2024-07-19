
#!/usr/bin/env python3
"""
This is a hypermedia pagination process.
"""
import csv
from typing import List, Tuple, Dict
import math


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """Fetches an index range in a page with the page size.
    """
    start = (page - 1) * page_size
    end = start + page_size
    return (start, end)


class Server:
    """A class server that paginate a database for popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        """Sets up a new server instance.
        """
        self.__dataset = None

    def dataset(self) -> List[List]:
        """A dataset cached.
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """Fetches a data in a page.
        """
        assert type(page) == int and type(page_size) == int
        assert page > 0 and page_size > 0
        start, end = index_range(page, page_size)
        data = self.dataset()
        if start > len(data):
            return []
        return data[start:end]

    def get_hyper(self, page: int = 1, page_size: int = 10) -> Dict:
        """Gets information in a page.
        """
        page_data = self.get_page(page, page_size)
        start, end = index_range(page, page_size)
        total_pages = math.ceil(len(self.__dataset) / page_size)
        page_info = {
            'page_size': len(page_data),
            'page': page,
            'data': page_data,
            'next_page': page + 1 if end < len(self.__dataset) else None,
            'prev_page': page - 1 if start > 0 else None,
            'total_pages': total_pages,
        }
        return page_info
