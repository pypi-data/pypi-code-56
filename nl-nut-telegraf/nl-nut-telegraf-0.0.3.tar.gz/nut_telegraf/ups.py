import json

from nut2 import PyNUTClient
from influxdb.line_protocol import make_line


class Label(object):
    def __init__(self, name, value):
        self.name = name
        self.value = value


class Tag(Label):
    pass


class Value(Label):
    pass


_export_status_map = {
    "OL": "On line (mains is present)",
    "OB": "On battery (mains is not present)",
    "LB": "Low battery",
    "HB": "High battery",
    "RB": "The battery needs to be replaced",
    "CHRG": "The battery is charging",
    "DISCHRG": "The battery is discharging (inverter is providing load power)",
    "BYPASS": "UPS bypass circuit is active - no battery protection is available",
    "CAL": "UPS is currently performing runtime calibration (on battery)",
    "OFF": "UPS is offline and is not supplying power to the load",
    "OVER": "UPS is overloaded",
    "TRIM": "UPS is trimming incoming voltage (called \"buck\" in some hardware)",
    "BOOST": "UPS is boosting incoming voltage",
    "FSD": "Forced Shutdown (restricted use, see the note below)",
}


_export_tags = {
    "device.mfr": {"device-make": str},
    "device.model": {"device-model": str},
    "device.serial": {"device-serial": str},
    "device.description": {"device-description": str},

    "battery.type": {"battery-type": str},

    # "input.voltage.nominal": {"input-voltage-nominal": float},
    # "output.voltage.nominal": {"output-voltage-nominal": float},
    # "battery.voltage.nominal": {"battery-voltage-nominal": float},
}

def _export_ups_status(prefix, sep):
    statuses = {prefix: str}
    for status_name in _export_status_map.keys():
        def st(status): return lambda l: status in l
        statuses[f'{prefix}{sep}{status_name}'] = st(status_name)
    return statuses

_export_measurements = {
    "input.voltage": {"input-voltage": float},
    "output.voltage": {"output-voltage": float},
    "battery.voltage": {"battery-voltage": float},

    "battery.charge": {"battery-charge": float},
    "battery.runtime": {"battery-runtime": float},
    "battery.runtime.low": {"battery-runtime-low": float},

    'ups.beeper.status': {
        "ups-beeper-status-enabled": lambda s: s == "enabled",
        "ups-beeper-status": str
    },

    'ups.delay.shutdown': {"ups-delay-shutdown": float},
    'ups.delay.start': {"ups-delay-start": float},
    'ups.load': {"ups-load": float},

    'ups.status': _export_ups_status("ups-status", "-"),
}


def _convert_metric(metric: str, value):
    labels = []
    if metric in _export_measurements:
        labels.extend([
            Value(name, v(value))
            for name, v in _export_measurements[metric].items()
        ])

    if metric in _export_tags:
        labels.extend([
            Tag(name, v(value))
            for name, v in _export_tags[metric].items()
        ])

    return labels


class IFLineP(object):
    @classmethod
    def value(cls, value):
        pass

    @classmethod
    def name(cls, value):
        pass

    @classmethod
    def tag_value(cls, value):
        pass

    @classmethod
    def field_value(cls, value):
        pass

    @staticmethod
    def _to_line_protocol(value):
        output = ""
        if isinstance(value, str):
            output = value
        else:
            output = "{}".format(value)

        for escape in [" ", ",", "="]:
            output.replace(escape, "\\{}".format(escape))


class NUTExporter(object):
    @classmethod
    def get_metrics(cls, host: str = "localhost", port: int = 3493, ups_name: str = None):
        client = PyNUTClient(
            host=host,
            port=port,
            timeout=5
        )

        return cls.parse(ups_name, client.list_vars(ups_name))

    @classmethod
    def parse(cls, ups_name: str, data: dict):
        out_tags = {"device-label": ups_name}
        out_values = {}

        for metric, value in data.items():
            for label in _convert_metric(metric, value):
                if isinstance(label, Tag):
                    out_tags[label.name] = label.value
                elif isinstance(label, Value):
                    out_values[label.name] = label.value

        return {
            "tags": out_tags,
            "measurements": out_values,
        }

    @classmethod
    def as_line_protocol(cls, m):
        return make_line(
            "ups-state",
            tags=m.get("tags", None),
            fields=m.get("measurements", None),
        )

    @classmethod
    def as_json(cls, m):
        return json.dumps(m)

