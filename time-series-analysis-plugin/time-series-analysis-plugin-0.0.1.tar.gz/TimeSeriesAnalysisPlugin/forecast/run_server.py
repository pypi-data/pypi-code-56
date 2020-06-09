from os import environ

from plugin_service.forecast.forecast_plugin_service import ForecastPluginService
from plugin_service.common.plugin_service import api, PluginModelAPI, PluginModelListAPI, PluginModelTrainAPI, \
    PluginModelInferenceAPI, PluginModelResultAPI, app, PluginModelParameterAPI

forecast = ForecastPluginService()

api.add_resource(PluginModelListAPI(forecast), '/forecast/models')
api.add_resource(PluginModelAPI(forecast), '/forecast/model', '/forecast/model/<model_key>')
api.add_resource(PluginModelTrainAPI(forecast), '/forecast/<model_key>/train')
api.add_resource(PluginModelInferenceAPI(forecast), '/forecast/<model_key>/inference')
api.add_resource(PluginModelResultAPI(forecast), '/forecast/<model_key>/result/query')
api.add_resource(PluginModelParameterAPI(forecast), '/forecast/parameters')

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', '0.0.0.0')
    PORT = environ.get('SERVER_PORT', 56789)
    app.run(HOST, PORT, threaded=True, use_reloader=False)
