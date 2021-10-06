import math
class Pagination:
    def __init__(self, list_size, page_size):
        self.current_page = 1
        self.list_size = list_size
        self.page_size = page_size
        