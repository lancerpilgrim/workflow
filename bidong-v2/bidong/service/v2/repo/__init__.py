# -*- coding: utf-8 -*-
"""
base repo

@author: Lancer
@date: 2017.9.4
"""
import time
from bidong.storage.models import (
    ResourceRegistry,
    ResourceTree,
)
from bidong.common.utils import ObjectDict, dictize
from bidong.core.database import session
from bidong.core.exceptions import InvalidParametersError


class BaseQuerySet(object):
    def all(self):
        """
         :return: vos iterable
         """
        return self._instantiate()

    def one(self):
        """
         for easy understand, essentially depends on the `_instantiate` function
         :return: single VO
         """
        return self._instantiate()

    def _instantiate(self, *args, **kwargs):
        raise NotImplementedError


class ResourcesQuery(BaseQuerySet):
    def __init__(self):
        self.r = None

    def filter_client(self):
        self.r = self.r.filter(ResourceRegistry.ascription == ResourceRegistry.CLIENT)
        return self

    def filter_platform(self):
        self.r = self.r.filter(ResourceRegistry.ascription == ResourceRegistry.PLATFORM)
        return self

    def get_all_resources(self):
        self.r = session.query(ResourceRegistry)
        return self

    def _instantiate(self, **kwargs):
        content = []
        for each in self.r.all():
            content.append(ObjectDict(dictize(each)))
        return content


_R_ID_MAP = {each.id: each for each in ResourcesQuery().get_all_resources().all()}
_R_NAME_MAP = {each.public_name: each for each in ResourcesQuery().get_all_resources().all()}


class ResourceQuery(BaseQuerySet):
    def __init__(self):
        self.r = None

    @staticmethod
    def locate_by_name(resource_name):
        try:
            return _R_NAME_MAP[resource_name]
        except KeyError:
            raise InvalidParametersError("Invalid Feature Name")

    @staticmethod
    def locate_by_id(_id):
        try:
            return _R_ID_MAP[_id]
        except KeyError:
            raise InvalidParametersError("Invalid Resource ID")

    def _instantiate(self):
        pass
