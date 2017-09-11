import math
from bidong.common.utils import ObjectDict


class Paginator(object):
    def __init__(self, query, page, page_size):
        self.query = query
        self.page = page
        self.page_size = page_size

    @property
    def total_items(self):
        return self.query.count()

    @property
    def total_pages(self):
        if self.page_size == 0:
            pages = 0
        else:
            pages = math.ceil(self.total_items / float(self.page_size))
        return pages

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def has_next(self):
        return self.page < self.total_pages

    @property
    def prev_num(self):
        if not self.has_prev:
            return None
        return self.page - 1

    @property
    def next_num(self):
        if not self.has_next:
            return None
        return self.page + 1

    @property
    def objects(self):
        query = self.query.limit(
            self.page_size
        ).offset((self.page - 1) * self.page_size)
        return query.all()

    @property
    def Query(self):
        query = self.query.limit(
            self.page_size
        ).offset((self.page - 1) * self.page_size)
        return query

    def to_dict(self):
        return {
            "next_page": self.next_num,
            "prev_page": self.prev_num,
            "total_pages": self.total_pages,
            "page": self.page,
            "page_size": self.page_size,
            "total_items": self.total_items,
            "objects": self.objects,
        }


paginator = ObjectDict({
    "page": None,
    "per_page": None,
    "order": "",
    "sort": ""
})
