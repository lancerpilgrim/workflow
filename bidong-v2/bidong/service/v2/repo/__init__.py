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


class ResourceRepo(BaseQuerySet):
    def __init__(self, resource_name="", resource_id=None):
        self.r = None
        self.resource_name = resource_name
        self.resource_id = resource_id

    def locate(self):
        if self.resource_id:
            self.r = session.query(ResourceRegistry).filter(ResourceRegistry.id == self.resource_id)
        else:
            self.r = session.query(ResourceRegistry).filter(
                ResourceRegistry.public_name == self.resource_name,
            )
        return self

    def _instantiate(self):
        return ObjectDict(dictize(self.r.one()))


class ResourcesRepo(BaseQuerySet):
    def __init__(self):
        self.r = None

    def generate_tree(self, resources):
        pass

    def expand_tree(self, resource_tree):
        pass

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


class ResourcesQuery(BaseQuerySet):
    def __init__(self):
        self.r = None

    def locate_by_name(self, resource_name):
        self.r = session.query(ResourceRegistry).filter(
            ResourceRegistry.public_name == resource_name)
        return self

    def exists(self):
        if self.r.first() is not None:
            return True
        return False

    def _instantiate(self):
        r = self.r.one_or_none()
        if r is None:
            return None
        return ObjectDict(dictize(self.r.one()))