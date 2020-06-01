from airflow.plugins_manager import AirflowPlugin

from .hook import NeuroHook
from .operator import BrowseLink, NeuroRunOperator
from .sensor import NeuroJobSensor, NeuroJobStatusSensor


class NeuroPlugin(AirflowPlugin):
    name = "neuro"

    # Will show up under airflow.hooks.neuro.NeuroHook
    hooks = [NeuroHook]
    # Will show up under airflow.operators.neuro.NeuroRunOperator
    operators = [NeuroRunOperator]
    # Will show up under airflow.sensors.neuro.NeuroJobSensor ...
    sensors = [NeuroJobSensor, NeuroJobStatusSensor]
    # Extra links
    operator_extra_links = [
        BrowseLink(),
    ]
