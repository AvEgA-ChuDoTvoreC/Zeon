# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - present by ChuDoTvoreC
"""
from datetime import datetime, timezone
from typing import List, Dict, Tuple


class ZabbixExportHeader:
    data = {
        "zabbix_export": {
            "version": "4.0",  # '3.4'  Current Zabbix version  (support JSON & XML import format)
            # isoformat(timespec="seconds") -> because python3.5.3 doesn't support timespec -> split used
            "date": str(datetime.now(timezone.utc).isoformat().split(".")[0]+"Z"),
        }
    }


class ZabbixExportInterface:

    @classmethod
    def data(cls, interface_info: List[Tuple[str, str, str]]):
        _data = {
            "interfaces": [
                {
                    "default": "1",
                    "type": "1",
                    "main": "1",  # must be here for host.create
                    "useip": "1",
                    "ip": ip or "127.0.0.1",
                    "dns": "",
                    "port": port or "10050",
                    "bulk": "1",
                    "interface_ref": ref or "if1"
                } for ip, port, ref in interface_info
            ]
        }
        return _data["interfaces"]


class ZabbixExportTemplates:

    @classmethod
    def data(cls, template_info: List[Tuple[str, str, List, List, List]]):
        _data = {
            "templates": [
                {
                    "template": template_name,
                    "name": template_name,
                    "description": description,
                    "groups": groups or "",
                    "applications": applications or "",
                    "items": items or "",
                    "discovery_rules": "",
                    "httptests": "",
                    "macros": "",
                    "templates": "",
                    "screens": ""
                } for template_name, description, groups, applications, items in template_info]
        }
        return _data["templates"]


class ZabbixExportGroups:

    @classmethod
    def data(cls, groups: List[str]):
        _data = {
            "groups": [
                {
                    "name": group_name
                } for group_name in groups
            ]
        }
        return _data["groups"]


class ZabbixExportApplications:

    @classmethod
    def data(cls, applications: List[str]):
        _data = {
            "applications": [
                {
                    "name": application_name
                } for application_name in applications
            ]
        }
        return _data["applications"]


class ZabbixExportItems:

    @classmethod
    def data(cls, items_info: List[Tuple[str, str, str, List, Dict]]):
        _data = {
            "items": [
                {
                    "name": item_name,
                    "type": item_type or "0",
                    "snmp_community": "",
                    "snmp_oid": "",
                    "key": key or "",
                    "delay": "30s",
                    "history": "90d",
                    "trends": "365d",
                    "status": "0",
                    "value_type": "3",
                    "allowed_hosts": "",
                    "units": "",
                    "snmpv3_contextname": "",
                    "snmpv3_securityname": "",
                    "snmpv3_securitylevel": "0",
                    "snmpv3_authprotocol": "0",
                    "snmpv3_authpassphrase": "",
                    "snmpv3_privprotocol": "0",
                    "snmpv3_privpassphrase": "",
                    "params": "",
                    "ipmi_sensor": "",
                    "authtype": "0",
                    "username": "",
                    "password": "",
                    "publickey": "",
                    "privatekey": "",
                    "port": "",
                    "description": "",
                    "inventory_link": "0",
                    "applications": applications or "",
                    "valuemap": "",
                    "logtimefmt": "",
                    "preprocessing": "",
                    "jmx_endpoint": "",
                    "timeout": "3s",
                    "url": "",
                    "query_fields": "",
                    "posts": "",
                    "status_codes": "200",
                    "follow_redirects": "1",
                    "post_type": "0",
                    "http_proxy": "",
                    "headers": "",
                    "retrieve_mode": "0",
                    "request_method": "0",
                    "output_format": "0",
                    "allow_traps": "0",
                    "ssl_cert_file": "",
                    "ssl_key_file": "",
                    "ssl_key_password": "",
                    "verify_peer": "0",
                    "verify_host": "0",
                    "master_item": master_item or ""
                } for item_name, item_type, key, applications, master_item in items_info
            ]
        }
        return _data["items"]
