# -*- coding: utf-8 -*-
"""
base repo

@author: Lancer
@date: 2017.1.4
"""


class BaseRepo(object):
    
    def all(self, page=1, per_page=20, sort="", order=""):
        """
         :return: vos iterable
         """
        return self._instantiate(page=page, per_page=per_page, sort=sort, order=order)

    def one(self):
        """
         for easy understand, essentially depends on the `_instantiate` function
         :return: single VO
         """
        return self._instantiate()

    def _instantiate(self, *args, **kwargs):
        raise NotImplementedError
