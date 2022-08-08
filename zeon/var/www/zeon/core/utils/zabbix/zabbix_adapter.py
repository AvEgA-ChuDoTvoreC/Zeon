# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - present by ChuDoTvoreC
"""
import json
from typing import Any, Dict, List

from pyzabbix import ZabbixAPI
from decouple import config

from core.utils.translator import Translator
from core.utils.zabbix.abstract_docs import AbstractCRUD, AbstractExportImport
from core.utils.zabbix.zabbix_schemas import ZabbixExportHeader, ZabbixExportTemplates, \
    ZabbixExportGroups, ZabbixExportApplications, ZabbixExportItems


ZC = {
    "url": "http://{zabbix_ip}/zabbix".format(zabbix_ip=config('ZABBIX_IP', default='192.168.74.53')),
    "user": config('ZABBIX_USER', default='Admin'),
    "password": config('ZABBIX_PASSWORD', default='zabbix')
}

ZABBIX_IMPORT_RULES = {
            "groups": {           #

                "createMissing": True

            },
            "hosts": {            #
                "updateExisting": True,
                "createMissing": True,

            },
            "templates": {        #
                "updateExisting": True,
                "createMissing": True

            },
            "templateScreens": {  #
                "updateExisting": False,
                "createMissing": False,
                "deleteMissing": False
            },
            "templateLinkage": {  #

                "createMissing": True,

            },
            "applications": {     #

                "createMissing": True,
                "deleteMissing": False
            },
            "items": {            #
                "updateExisting": True,
                "createMissing": True,
                "deleteMissing": False
            },
            "discoveryRules": {   #
                "updateExisting": True,
                "createMissing": True,
                "deleteMissing": False
            },
            "triggers": {         #
                "updateExisting": True,
                "createMissing": True,
                "deleteMissing": False
            },
            "graphs": {           #
                "updateExisting": True,
                "createMissing": True,
                "deleteMissing": False
            },
            # "webScenarios": {     # TODO: find correct key for Web Scenario
            #     "updateExisting": True,
            #     "createMissing": True,
            #     "deleteMissing": False
            # },
            "screens": {          #
                "updateExisting": False,
                "createMissing": False,

            },
            "maps": {             #
                "updateExisting": False,
                "createMissing": False,

            },
            "images": {           #
                "updateExisting": False,
                "createMissing": False,

            },
            "valueMaps": {    # ?
                "updateExisting": False,
                "createMissing": True,

            }
        }


# ZABBIX ADAPTER API CLASS MIXINS
class CRUDMixin(AbstractCRUD):
    """
        Intermediate class that helps build string for Zabbix API via dot notation.
        Extends Base class with 'CRUD' methods
    """

    def __init__(self, module_name, zabbix_adapter):
        self._module_name = module_name
        self._zabbix_adapter = zabbix_adapter

    def get(self, **kwargs) -> List:
        method = '{0}.{1}'.format(self._module_name, self.get.__name__)
        if kwargs:
            return self._zabbix_adapter.import_template(method=method)(**kwargs)
        return self._zabbix_adapter.import_template(method=method)()

    def create(self, **kwargs) -> Dict:
        method = '{0}.{1}'.format(self._module_name, self.create.__name__)
        return self._zabbix_adapter.import_template(method=method)(**kwargs)

    def delete(self, *args) -> List:
        method = '{0}.{1}'.format(self._module_name, self.delete.__name__)
        return self._zabbix_adapter.import_template(method=method)(*args)

    def update(self, **kwargs) -> Dict:
        method = '{0}.{1}'.format(self._module_name, self.update.__name__)
        return self._zabbix_adapter.import_template(method=method)(**kwargs)


class ExportImportMixin(AbstractExportImport):
    """
        Intermediate class that helps build string for Zabbix API via dot notation.
        Extends Base class with 'export/import' methods.
    """

    def __init__(self, module_name, zabbix_adapter):
        self._module_name = module_name
        self._zabbix_adapter = zabbix_adapter

    def export(self, host_id: str):
        method = '{0}.{1}'.format(self._module_name, self.export.__name__)
        return self._zabbix_adapter.import_template(method=method)(
            format="json",
            options={"hosts": [host_id]}
        )

    def import_(self, source: dict):
        method = '{0}.{1}'.format(self._module_name, self.import_.__name__[:-1])
        return self._zabbix_adapter.import_template(method=method)(
            format="json",
            rules=ZABBIX_IMPORT_RULES,
            source=json.dumps(source)
        )


# ZABBIX ADAPTER API CLASS METHODS
class Configuration(ExportImportMixin):
    pass


class Host(CRUDMixin):
    pass


class HostGroups(CRUDMixin):
    pass


class HostTemplates(CRUDMixin):
    pass


class HostInterfaces(CRUDMixin):
    pass


class HostApplications(CRUDMixin):
    pass


class ApplicationItems(CRUDMixin):
    pass


class ZabbixAdapter:
    """
        The Last class in chain that helps build string for Zabbix API via dot notation.
        ZabbixAdapter runs __getattr__ from ZabbixAPI class which dynamically create an object class (ie: host),
        ZabbixAPI runs __getattr__ from ZabbixAPIObjectClass which dynamically create a method (ie: get).
        As a last step subclasses (CRUDMixin, Configuration or any child) pass *args & **kwargs to
        'import_template' method.
    """

    def __init__(self, **kwargs):
        self.zapi = ZabbixAPI(kwargs["url"])
        self.zapi.login(user=kwargs["user"], password=kwargs["password"])

    def execute(self, dotted_cmd: str) -> Any:
        try:
            module, method = dotted_cmd.rsplit('.', 1) if len(dotted_cmd.rsplit('.')) == 2 else TypeError
        except (ValueError, TypeError) as err:
            raise ImportError("%s doesn't look like a module" % dotted_cmd) from err

        try:
            return getattr(getattr(self.zapi, module), method)
        except AttributeError as err:
            raise ImportError('Module "%s" does not define a "%s" attribute/class' % (
                module, method)
            ) from err

    def import_template(self, method):
        return self.execute(dotted_cmd=method)


class ZabbixAdapterAPI:
    """
        Base class that helps build string for Zabbix API via dot notation.
    """
    def __init__(self):
        self._zabbix_adapter = ZabbixAdapter(**ZC)

    @property
    def configuration(self):
        """Choose next method..."""
        return Configuration("configuration", self._zabbix_adapter)

    @property
    def host(self):
        """Choose next method..."""
        return Host("host", self._zabbix_adapter)

    @property
    def hostgroup(self):
        """Choose next method..."""
        return HostGroups("hostgroup", self._zabbix_adapter)

    @property
    def template(self):
        """Choose next method..."""
        return HostTemplates("template", self._zabbix_adapter)

    @property
    def hostinterface(self):
        """Choose next method..."""
        return HostInterfaces("hostinterface", self._zabbix_adapter)

    @property
    def application(self):
        """Choose next method..."""
        return HostApplications("application", self._zabbix_adapter)

    @property
    def item(self):
        """Choose next method..."""
        return ApplicationItems("item", self._zabbix_adapter)


class Creator:

    def __init__(self):
        self.translator = Translator()

        self._export = None
        self._groups = None
        self._templates = None
        self._items = None

    def create_export_json(self, groups_in_export, templates_in_export):

        # SET ZABBIX_EXPORT HEADER
        self._export = ZabbixExportHeader.data

        # UPDATE ZABBIX_EXPORT WITH TEMPLATES AND GROUPS
        zabbix_export_header = self._export["zabbix_export"]
        zabbix_export_header.update(
            {
                "groups": ZabbixExportGroups.data(groups=groups_in_export)  # All Templates Groups
            }
        )
        zabbix_export_header.update(
            {
                "templates": templates_in_export  # All Templates
            }
        )
        return self._export

    def create_template_json(self, template_name, template_description, template_group, applications_in_template, items_in_template):

        self._templates = ZabbixExportTemplates.data(
            template_info=[
                (
                    template_name,
                    template_description,
                    ZabbixExportGroups.data(groups=template_group),                        # Curr Template Groups
                    ZabbixExportApplications.data(applications=applications_in_template),  # Curr Template Applications
                    items_in_template                                                      # Curr Template Items
                )
            ]
        )
        return self._templates

    def create_item_json(self, item_name, item_application, key):

        key_state = key + ".state"
        key_msg = key + ".msg"
        slaves_info = [("state", key_state), ("msg", key_msg)]

        type_zabbix = "0"
        type_dependent = "18"

        self._items = ZabbixExportItems.data(
            items_info=[
                # Master Item
                (
                    item_name,
                    type_zabbix,
                    key,
                    ZabbixExportApplications.data(applications=item_application),  # Current Item Application
                    {}                # master_item
                ),
                # Slaves unpack
                *[
                    (
                        _slave_name,
                        type_dependent,
                        _key_state,
                        ZabbixExportApplications.data(applications=item_application),  # Current Item Application
                        {"key": key}  # link to master_item
                    ) for _slave_name, _key_state in slaves_info
                ]
            ]
        )
        return self._items

    def generate_template(self, data: dict):
        _groups_in_template = list()
        _templates_in_export = list()

        for template_name in data.keys():

            _items_in_template = list()
            _applications_in_template = list()

            for application_name in data[template_name]:

                _applications_in_template.append(application_name)

                for item_name in data[template_name][application_name]:
                    _key = ".".join([template_name, application_name, item_name])
                    _item = self.create_item_json(
                        item_name=item_name,
                        item_application=[application_name],
                        key=self.translator.ru_cyr_to_lat(_key).replace(" ", "_").replace("/", "-").lower()
                    )
                    _items_in_template.extend(_item)

            _template_group = ["Templates/{}_System".format(template_name)]
            _template = self.create_template_json(
                template_name=self.translator.ru_cyr_to_lat(template_name),
                template_description="My {} Template Description".format(template_name),
                applications_in_template=_applications_in_template,
                template_group=_template_group,
                items_in_template=_items_in_template
            )
            _templates_in_export.extend(_template)
            _groups_in_template.extend(_template_group)

        _export = self.create_export_json(
            groups_in_export=_groups_in_template,
            templates_in_export=_templates_in_export
        )
        return _export

