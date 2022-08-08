# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - present by ChuDoTvoreC
"""
from core.utils.zabbix.abstract_docs import AbstractFilter


class Filter(AbstractFilter):

    @classmethod
    def by_name(cls, name: str, **kwargs):
        filter_by_name_template = {
            "filter": {
                "name": name
            },
            "output": ["itemid"]
        }
        filter_by_name_template.update(kwargs)
        return filter_by_name_template

    @classmethod
    def by_id(cls, filter_key: str, itemid: str, **kwargs):
        filter_by_name_template = {
            "filter": {
                filter_key: itemid
            },
            "output": ["itemid"]
        }
        filter_by_name_template.update(kwargs)
        return filter_by_name_template
