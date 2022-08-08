# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - present by ChuDoTvoreC
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List


class AbstractCRUD(ABC):

    @abstractmethod
    def get(self, filter: Dict, output: List) -> List:
        """
        Example:

            Use 'filter' by name or groupid:

            >>> get(filter={"itemid": "321"})
            >>> get(filter={"name": ["Name1", "Name2"]})

            >>> get(filter={"groupid": ["1", "2"]]})
            >>> get(filter={"hostid": "10256"})
            >>> get(filter={"applicationid": "443"})
            >>> get(filter={"templateid": "192"})

            Use 'output' to change it:

            >>> get(output=["itemid", "name"])


        https://zabbix.com/documentation
        """
        pass

    @abstractmethod
    def create(self,  name: str) -> dict:
        """
        Example:

            Use 'name' to set it:

            >>> create(name="Name")

        https://zabbix.com/documentation
        """
        pass

    @abstractmethod
    def update(self, item_id: str, new_name: str) -> list:
        """
        Example:

            Use 'item_id' and 'new_name' to rename item:

            >>> update(item_id="32", new_name="New Group Name")

        https://zabbix.com/documentation
        """
        pass

    @abstractmethod
    def delete(self, *args) -> list:
        """
        Example:

            Insert ids to delete them:

            >>> delete("32", "33", "34")

        https://zabbix.com/documentation
        """
        pass


class AbstractExportImport(ABC):

    @abstractmethod
    def export(self, host_id: str):
        """Exports source configuration from Zabbix Server"""
        pass

    @abstractmethod
    def import_(self, source: dict):
        """Import source configuration to Zabbix Server"""
        pass


class AbstractFilter(ABC):

    @abstractmethod
    def by_name(self, name: str, hostids: str):
        pass
