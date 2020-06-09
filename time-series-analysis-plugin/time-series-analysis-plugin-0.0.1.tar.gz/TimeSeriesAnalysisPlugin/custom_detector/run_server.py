from os import environ
from flask import request

from plugin_service.custom_detector.custom_detector_plugin_service import CustomDetectorPluginService
from plugin_service.common.plugin_service import api, PluginModelAPI, PluginModelListAPI, PluginModelTrainAPI, \
    PluginModelInferenceAPI, PluginModelResultAPI, app, PluginModelParameterAPI

customdetector = CustomDetectorPluginService()

api.add_resource(PluginModelListAPI(customdetector), '/customdetector/models')
api.add_resource(PluginModelAPI(customdetector), '/customdetector/model', '/customdetector/model/<model_key>')
api.add_resource(PluginModelInferenceAPI(customdetector), '/customdetector/<model_key>/select')
api.add_resource(PluginModelResultAPI(customdetector), '/customdetector/<model_key>/result/query')
api.add_resource(PluginModelParameterAPI(customdetector), '/customdetector/parameters')


if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', '127.0.0.1')
    PORT = environ.get('SERVER_PORT', 56789)
    app.run(HOST, PORT, threaded=True, use_reloader=False)
