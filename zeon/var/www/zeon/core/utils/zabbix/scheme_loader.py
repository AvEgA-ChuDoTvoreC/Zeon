import json
from typing import List, Any, Dict

from core.utils.translator import Translator
from core.utils.zabbix.zabbix_filters import Filter
from core.utils.zabbix.zabbix_schemas import ZabbixExportInterface
from core.utils.zabbix.zabbix_adapter import ZabbixAdapterAPI, Creator


class DataParser:

    def __init__(self, measurements, host_creds: Dict):
        self.measurements = measurements
        self.host_creds = host_creds

        self._keys = None
        self._result = None
        self._create_zab_template = None
        self._import_zab_template = None
        self._zab_host = None

        self._adapterAPI = None
        self._creator = None
        self._translator = None

    def proceed(self):
        self._adapterAPI = ZabbixAdapterAPI()
        self._creator = Creator()
        self._translator = Translator()

        self._keys = self.gather_keys(
            measurements=self.measurements,
            system=self.host_creds.get("system")
        )
        self._result = dict(self.setup_dict(self._keys).items())
        self._create_zab_template = self._creator.generate_template(data=self._result)
        self._import_zab_template = self._adapterAPI.configuration.import_(self._create_zab_template)
        return self

    def push_to_zabbix(self):
        self._zab_host = self.create_host_and_update_it_with_new_template_via_zabbix_api(**self.host_creds)
        return self

    def result(self):
        return bool(self._zab_host)

    def print_results(self) -> None:
        print("keys:        \t", self._keys)
        print("res:         \t", self._result)
        print("res dump:", json.dumps(self._result, indent=4, sort_keys=False, ensure_ascii=False))
        print("created template:", json.dumps(self._create_zab_template, indent=4, sort_keys=False, ensure_ascii=False))
        print("import_result:", self._import_zab_template)
        print("zab_host:", self._zab_host)

    @staticmethod
    def retrieve_id(filter_key: str, instance: Any, many=False) -> str or list:
        if instance:
            if not many:
                try:
                    return instance[0][filter_key]
                except KeyError:
                    return instance[filter_key + "s"][0]
            else:
                # FIXME: Hardcode -> только один случай рассмотрен для запроса шаблонов хоста
                try:
                    return [instance_element[filter_key] for instance_element in instance[0]["parentTemplates"]]
                except KeyError:
                    return [instance_element[filter_key + "s"] for instance_element in instance[0]["parentTemplates"]]
        return ""

    @staticmethod
    def setup_dict(data: List[tuple]):
        d = dict()
        # FIXME: replace method should be at util --> add function to correct incoming string
        for head, body, tail in data:
            d.setdefault(head.replace("/", "_"), dict()).setdefault(body, list()).append(tail)
        return d

    @staticmethod
    def gather_keys(measurements: List[dict], system: str) -> List[tuple]:
        return [tuple((system, _sensor.get("subsystem"), _sensor.get("data").get("msg"))) for _sensor in measurements]

    def create_host_and_update_it_with_new_template_via_zabbix_api(self, **kwargs):

        # Host
        host_name = kwargs.get("host_name")
        host_group_name = kwargs.get("host_group_name")
        ip = "127.0.0.1"
        port = "10050"
        interface_ref = "if1"

        # Template
        # FIXME: replace here and at setup_dict() ----> change it
        template_name = self._translator.ru_cyr_to_lat(kwargs.get("system")).replace("/", "_")

        # UPDATE HOST WITH NEW_TEMPLATE (CREATED BEFORE)
        hostid = DataParser.retrieve_id(
            "hostid",
            self._adapterAPI.host.get(**Filter.by_name(name=host_name))
        )
        host_templates = DataParser.retrieve_id(
            "templateid",
            self._adapterAPI.host.get(**Filter.by_name(name=host_name, output="parentTemplates", selectParentTemplates=['templateid', 'name'])),
            many=True
        )
        templateid1 = DataParser.retrieve_id(
            "templateid",
            self._adapterAPI.template.get(**Filter.by_name(name=template_name))
        )
        groupid = DataParser.retrieve_id(
            "groupid",
            self._adapterAPI.hostgroup.get(**Filter.by_name(name=host_group_name))
        )

        all_interfaces = ZabbixExportInterface.data(
            interface_info=[
                (
                    ip,
                    port,
                    interface_ref
                )
            ]
        )

        if not groupid:
            groupid = DataParser.retrieve_id("groupid", self._adapterAPI.hostgroup.create(
                name=host_group_name
            ))

        if not hostid:
            hostid = DataParser.retrieve_id("hostid", self._adapterAPI.host.create(
                host=host_name,
                interfaces=all_interfaces,
                groups=[{"groupid": groupid}],
                # templates=[{"templateid": templateid}],
                **kwargs
            ))

            return DataParser.retrieve_id("hostid", self._adapterAPI.host.update(
                hostid=hostid,
                templates=[
                    {"templateid": templateid1}
                ],
                **kwargs
            ))

        templates_ids = [{"templateid": t_id} for t_id in host_templates if t_id]
        templates_ids.append({"templateid": templateid1})

        return DataParser.retrieve_id("hostid", self._adapterAPI.host.update(
            hostid=hostid,
            templates=templates_ids,
            **kwargs
        ))
