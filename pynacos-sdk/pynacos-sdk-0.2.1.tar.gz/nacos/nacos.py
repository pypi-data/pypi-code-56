from winney import Winney
from typing import Dict, List

from .errors import RequestError, ParamError
from .entities import (Entity, ServiceEntity, ServiceListEntity,
                       InstanceEntity, HostEntity, InstanceListEntity,
                       ServerEntity, LeaderEntity, MetricsEntity)
from .params import (Param, ServiceRegisterParam, ServiceRemoveParam,
                     ServiceUpdateParam, ServiceGetParam, ServiceListParam,
                     SwitchUpdateParam, InstanceRegisterParam,
                     InstanceRemoveParam, InstanceUpdateParam,
                     InstanceListParam, InstanceGetParam, BeatInfo,
                     InstanceBeatParam, HealthUpdateParam, ServerListParam,
                     ConfigGetParam, ConfigListenParam, ConfigPublishParam,
                     ConfigRemoveParam)


class Nacos(object):
    def __init__(self, host, port, namespace_id):
        self.winney = Winney(
            host=host,
            port=port,
        )
        self.init_functions()
        self.namespace_id = namespace_id

    def init_functions(self):
        # 配置
        self.winney.register(method="get",
                             name="config_get",
                             uri="/nacos/v1/cs/configs")
        self.winney.register(method="post",
                             name="config_listen",
                             uri="/nacos/v1/cs/configs/listener")
        self.winney.register(method="post",
                             name="config_publish",
                             uri="/nacos/v1/cs/configs")
        self.winney.register(method="delete",
                             name="config_remove",
                             uri="/nacos/v1/cs/configs")

        # 服务
        self.winney.register(method="post",
                             name="service_register",
                             uri="/nacos/v1/ns/service")
        self.winney.register(method="delete",
                             name="service_remove",
                             uri="/nacos/v1/ns/service")
        self.winney.register(method="put",
                             name="service_update",
                             uri="/nacos/v1/ns/service")
        self.winney.register(method="get",
                             name="service_get",
                             uri="/nacos/v1/ns/service")
        self.winney.register(method="get",
                             name="service_list",
                             uri="/nacos/v1/ns/service/list")

        # 开关
        self.winney.register(method="get",
                             name="switch_get",
                             uri="/nacos/v1/ns/operator/switches")
        self.winney.register(method="put",
                             name="switch_update",
                             uri="/nacos/v1/ns/operator/switches")

        # 实例
        self.winney.register(method="post",
                             name="instance_register",
                             uri="/nacos/v1/ns/instance")
        self.winney.register(method="delete",
                             name="instance_remove",
                             uri="/nacos/v1/ns/instance")
        self.winney.register(method="put",
                             name="instance_update",
                             uri="/nacos/v1/ns/instance")
        self.winney.register(method="get",
                             name="instance_list",
                             uri="/nacos/v1/ns/instance/list")
        self.winney.register(method="get",
                             name="instance_get",
                             uri="/nacos/v1/ns/instance")
        self.winney.register(method="put",
                             name="instance_beat",
                             uri="/nacos/v1/ns/instance/beat")

        # 其他
        self.winney.register(method="get",
                             name="metrics_get",
                             uri="/nacos/v1/ns/operator/metrics")
        self.winney.register(method="get",
                             name="server_list",
                             uri="/nacos/v1/ns/operator/servers")
        self.winney.register(method="get",
                             name="leader_get",
                             uri="/nacos/v1/ns/raft/leader")
        self.winney.register(method="put",
                             name="health_update",
                             uri="/nacos/v1/ns/health/instance")

    # 处理参数
    def get_params(self, param: Param) -> Dict:
        if not isinstance(param, Param):
            raise ParamError(
                "param should be type of Param, but {} found".format(
                    type(param)))
        params = param.json()
        params["namespaceId"] = self.namespace_id
        return params

    # 注册服务
    def service_register(self, param: ServiceRegisterParam) -> bool:
        if not isinstance(param, ServiceRegisterParam):
            raise ParamError(
                "param should be type of ServiceRegisterParam, but {} found".
                format(type(param)))
        params = self.get_params(param)
        r = self.winney.service_register(data=params)
        if not r.ok():
            raise RequestError(
                "failed to register service, http status = {}".format(
                    r.status_code))
        return True

    # 删除服务
    def service_remove(self, param: ServiceRemoveParam) -> bool:
        if not isinstance(param, ServiceRemoveParam):
            raise ParamError(
                "param should be type of ServiceRemoveParam, but {} found".
                format(type(param)))
        params = self.get_params(param)
        r = self.winney.service_remove(data=params)
        if not r.ok():
            raise RequestError(
                "failed to remove service, http status = {}".format(
                    r.status_code))
        return True

    # 更新服务
    def service_update(self, param: ServiceUpdateParam) -> bool:
        if not isinstance(param, ServiceUpdateParam):
            raise ParamError(
                "param should be type of ServiceUpdateParam, but {} found".
                format(type(param)))
        params = self.get_params(param)
        r = self.winney.service_update(data=params)
        if not r.ok():
            raise RequestError(
                "failed to update service, http status = {}".format(
                    r.status_code))
        return True

    # 获取服务详情
    def service_get(self, param: ServiceGetParam) -> ServiceEntity:
        if not isinstance(param, ServiceGetParam):
            raise ParamError(
                "param should be type of ServiceGetParam, but {} found".format(
                    type(param)))
        params = self.get_params(param)
        r = self.winney.service_get(data=params)
        if not r.ok():
            raise RequestError(
                "failed to get service, http status = {}".format(
                    r.status_code))
        return ServiceEntity.loads(**r.json())

    # 获取服务列表
    def service_list(self, param: ServiceListParam) -> ServiceListEntity:
        if not isinstance(param, ServiceListParam):
            raise ParamError(
                "param should be type of ServiceListParam, but {} found".
                format(type(param)))
        params = self.get_params(param)
        r = self.winney.service_list(data=params)
        if not r.ok():
            raise RequestError(
                "failed to list service, http status = {}".format(
                    r.status_code))
        return ServiceListEntity.loads(**r.json())

    # 获取系统开关
    def switch_get(self) -> Dict:
        r = self.winney.switch_get()
        if not r.ok():
            raise RequestError("failed to get switch, http status = {}".format(
                r.status_code))
        return r.json()

    # 更新系统开关
    def switch_update(self, param: SwitchUpdateParam) -> bool:
        if not isinstance(param, SwitchUpdateParam):
            raise ParamError(
                "param should be type of SwitchUpdateParam, but {} found".
                format(type(param)))
        params = self.get_params(param)
        r = self.winney.service_list(data=params)
        if not r.ok():
            raise RequestError(
                "failed to update switch, http status = {}".format(
                    r.status_code))
        return True

    # 注册实例
    def instance_register(self, param: InstanceRegisterParam) -> bool:
        if not isinstance(param, InstanceRegisterParam):
            raise ParamError(
                "param should be type of InstanceRegisterParam, but {} found".
                format(type(param)))
        params = self.get_params(param)
        r = self.winney.instance_register(data=params)
        if not r.ok():
            raise RequestError(
                "failed to register instance, http status = {}".format(
                    r.status_code))
        return True

    # 删除实例
    def instance_remove(self, param: InstanceRemoveParam) -> bool:
        if not isinstance(param, InstanceRemoveParam):
            raise ParamError(
                "param should be type of InstanceRemoveParam, but {} found".
                format(type(param)))
        params = self.get_params(param)
        r = self.winney.instance_remove(data=params)
        if not r.ok():
            raise RequestError(
                "failed to remove instance, http status = {}".format(
                    r.status_code))
        return True

    # 更新实例
    def instance_update(self, param: InstanceUpdateParam) -> bool:
        if not isinstance(param, InstanceUpdateParam):
            raise ParamError(
                "param should be type of InstanceUpdateParam, but {} found".
                format(type(param)))
        params = self.get_params(param)
        r = self.winney.instance_update(data=params)
        if not r.ok():
            raise RequestError(
                "failed to update instance, http status = {}".format(
                    r.status_code))
        return True

    # 查询服务下的实例列表
    def instance_list(self, param: InstanceListParam) -> InstanceListEntity:
        if not isinstance(param, InstanceListParam):
            raise ParamError(
                "param should be type of InstanceListParam, but {} found".
                format(type(param)))
        params = self.get_params(param)
        r = self.winney.instance_list(data=params)
        if not r.ok():
            raise RequestError(
                "failed to list instance, http status = {}".format(
                    r.status_code))
        return InstanceListEntity.loads(**r.json())

    # 获取实例详情
    def instance_get(self, param: InstanceGetParam) -> InstanceEntity:
        if not isinstance(param, InstanceGetParam):
            raise ParamError(
                "param should be type of InstanceGetParam, but {} found".
                format(type(param)))
        params = self.get_params(param)
        r = self.winney.instance_get(data=params)
        if not r.ok():
            raise RequestError(
                "failed to get instance, http status = {}".format(
                    r.status_code))
        return InstanceEntity.loads(**r.json())

    # 实例发送心跳
    def instance_beat(self, beat_info: BeatInfo) -> bool:
        if not isinstance(beat_info, BeatInfo):
            raise ParamError(
                "beat_info should be type of BeatInfo, but {} found".format(
                    type(beat_info)))
        param = InstanceBeatParam(beat_info)
        params = self.get_params(param)
        r = self.winney.instance_beat(data=params)
        if not r.ok():
            raise RequestError(
                "failed to beat instance, http status = {}".format(
                    r.status_code))
        return True

    # 查看系统当前数据指标
    def metrics_get(self) -> MetricsEntity:
        r = self.winney.metrics_get()
        if not r.ok():
            raise RequestError(
                "failed to get metrics, http status = {}".format(
                    r.status_code))
        return MetricsEntity.loads(**r.json())

    # 查看集群 server 列表
    def server_list(self, param: ServerListParam) -> List[ServerEntity]:
        if not isinstance(param, ServerListParam):
            raise ParamError(
                "param should be type of ServerListParam, but {} found".format(
                    type(param)))
        params = self.get_params(param)
        r = self.winney.instance_get(data=params)
        if not r.ok():
            raise RequestError(
                "failed to list server, http status = {}".format(
                    r.status_code))
        servers = r.json()["servers"]
        servers = [ServerEntity.loads(**server)
                   for server in servers] if servers else []
        return servers

    # 查看当前集群 leader
    def leader_get(self) -> LeaderEntity:
        r = self.winney.leader_get()
        if not r.ok():
            raise RequestError("failed to get leader, http status = {}".format(
                r.status_code))
        return LeaderEntity.loads(**r.json())

    # 更新实例的健康状态
    def health_update(self, param: HealthUpdateParam) -> bool:
        if not isinstance(param, HealthUpdateParam):
            raise ParamError(
                "param should be type of HealthUpdateParam, but {} found".
                format(type(param)))
        params = self.get_params(param)
        r = self.winney.health_update(data=params)
        if not r.ok():
            raise RequestError(
                "failed to update health, http status = {}".format(
                    r.status_code))
        return True

    # 获取配置
    def config_get(self, param: ConfigGetParam) -> str:
        if not isinstance(param, ConfigGetParam):
            raise ParamError(
                "param should be type of ConfigGetParam, but {} found".format(
                    type(param)))
        params = param.to_json(namespace_id=self.namespace_id)
        r = self.winney.config_get(data=params)
        if not r.ok():
            raise RequestError("failed to get config, http status = {}".format(
                r.status_code))
        return r.get_text()

    # 监听配置
    def config_listen(self, param: ConfigListenParam) -> str:
        """监听 30s，返回空串表示无变化"""
        if not isinstance(param, ConfigListenParam):
            raise ParamError(
                "param should be type of ConfigListenParam, but {} found".
                format(type(param)))
        params = param.to_json(self.namespace_id)
        r = self.winney.config_listen(
            data=params, headers={"Long-Pulling-Timeout": "30000"})
        if not r.ok():
            raise RequestError(
                "failed to listen config, http status = {}".format(
                    r.status_code))
        return r.get_text()

    # 发布配置
    def config_publish(self, param: ConfigPublishParam) -> bool:
        if not isinstance(param, ConfigPublishParam):
            raise ParamError(
                "param should be type of ConfigPublishParam, but {} found".
                format(type(param)))
        params = param.to_json(namespace_id=self.namespace_id)
        r = self.winney.config_publish(data=params)
        if not r.ok():
            raise RequestError(
                "failed to publish config, http status = {}".format(
                    r.status_code))
        return True

    # 删除配置
    def config_remove(self, param: ConfigRemoveParam) -> bool:
        if not isinstance(param, ConfigRemoveParam):
            raise ParamError(
                "param should be type of ConfigRemoveParam, but {} found".
                format(type(param)))
        params = param.to_json(namespace_id=self.namespace_id)
        r = self.winney.config_remove(data=params)
        if not r.ok():
            raise RequestError(
                "failed to remove config, http status = {}".format(
                    r.status_code))
        return True
