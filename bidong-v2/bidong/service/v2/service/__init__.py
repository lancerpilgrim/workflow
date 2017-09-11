from bidong.core.paginator import paginator


class BaseCollectionService(object):

    def __init__(self):
        self.paginator = paginator

    def paginate(self, page, per_page, sort="", order=""):
        self.paginator.update({
            "page": page, "per_page": per_page, "sort": sort, "order": order
        })
        return self


class BaseIndividualService(object):
    pass