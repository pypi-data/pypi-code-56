from common.plugin_service import PluginService
from common.util.constant import STATUS_SUCCESS, STATUS_FAIL
from common.util.timeutil import get_time_offset, str_to_dt, dt_to_str
from common.util.csv import save_csv
import json
import shutil
import os

class ForecastPluginService(PluginService):

    def __init__(self):
        super().__init__()

    # Verify if the data could be used for this application
    # Parameters: 
    #   series_sets: a array of series set
    #   parameters: parameters of this application.
    # Return:
    #   result:  STATUS_FAIL / STATUS_SUCCESS
    #   message: a description of the result
    def do_verify(self, parameters):
        # ------TO BE REPLACED: Other application just replace below part-------
        # For forecast, check the factors and target has same granularity, and each factor could only contain one series
        meta = self.tsanaclient.get_metric_meta(parameters['instance']['params']['target']['metricId'])
        if meta is None: 
            return STATUS_FAIL, 'Target is not found. '
        target_gran = meta['granularityName']
        # Only for custom, the granularity amount is meaningful which is the number of seconds
        target_gran_amount = meta['granularityAmount']

        for data in parameters['seriesSets']: 
            if target_gran != data['metricMeta']['granularityName'] or (target_gran == 'Custom' and target_gran_amount != data['metricMeta']['granularityAmount']):
                return STATUS_FAIL, 'Granularity must be identical between target and factors. '

        # Check series count, and each factor should only contain 1 series
        seriesCount = 0
        for data in parameters['seriesSets']: 
            dim = {}
            for dimkey in data['dimensionFilter']: 
                dim[dimkey] = [data['dimensionFilter'][dimkey]]
            
            dt = dt_to_str(str_to_dt(meta['dataStartFrom']))
            para = dict(metricId=data['metricId'], dimensions=dim, count=2, startTime=dt)     # Let's said 100 is your limitation
            response = self.tsanaclient.post('/metrics/' + data['metricId'] + '/rank-series', data=para)
            ret = response.json()
            if ret is None or response.status_code != 200 or 'value' not in ret:
                return STATUS_FAIL, 'Read series rank filed. '
            seriesCount += len(ret['value'])
            if seriesCount > self.config.series_limit:
                return STATUS_FAIL, 'Cannot accept ambiguous factors or too many series in the group, limit is ' + str(self.config.series_limit) + '.'

        return STATUS_SUCCESS, ''

    def prepare_data(self, parameters, model_key, time_key):
        inference_window = parameters['instance']['params']['windowSize']
        # meta = get_metric_meta(self.config, parameters['instance']['params']['target']['metricId'])
        meta = self.tsanaclient.get_metric_meta(parameters['instance']['params']['target']['metricId'])
        if meta is None:
            raise Exception('Metric is not found.')

        end_time = str_to_dt(parameters['endTime'])
        if 'startTime' in parameters:
            start_time = str_to_dt(parameters['startTime'])
        else:
            start_time = end_time

        data_end_time = get_time_offset(end_time, (meta['granularityName'], meta['granularityAmount']),
                                        + 1)
        data_start_time = get_time_offset(start_time, (meta['granularityName'], meta['granularityAmount']),
                                          - inference_window * 2)

        factor_def = parameters['seriesSets']
        # factors_data = get_timeseries(self.config, factor_def, data_start_time, data_end_time)
        factors_data = self.tsanaclient.get_timeseries(factor_def, data_start_time, data_end_time)

        target_def = [parameters['instance']['params']['target']]
        # target_data = get_timeseries(self.config, target_def, data_start_time, data_end_time)
        target_data = self.tsanaclient.get_timeseries(target_def, data_start_time, data_end_time)

        data_dir = os.path.join(self.config.model_data_dir, model_key, time_key)
        shutil.rmtree(data_dir, ignore_errors=True)
        os.makedirs(data_dir, exist_ok=True)

        for target in target_data:
            csv_file = os.path.join(data_dir, target.series_id + '.csv')
            save_csv([(tuple['timestamp'], tuple['value']) for tuple in target.value], csv_file)

        for factor in factors_data:
            csv_file = os.path.join(data_dir, factor.series_id + '.csv')
            save_csv([(tuple['timestamp'], tuple['value']) for tuple in factor.value], csv_file)

        return data_dir


    def do_train(self, model_key, model_dir, parameters):
        return STATUS_SUCCESS, ''

    def do_state(self, model_key):
        return STATUS_SUCCESS, ''

    def do_inference(self, model_key, model_dir, parameters):
        inference_window = parameters['instance']['params']['windowSize']
        # meta = get_metric_meta(self.config, parameters['instance']['params']['target']['metricId'])
        meta = self.tsanaclient.get_metric_meta(parameters['instance']['params']['target']['metricId'])
        if meta is None:
            raise Exception('Metric is not found.')

        end_time = str_to_dt(parameters['endTime'])
        if 'startTime' in parameters:
            start_time = str_to_dt(parameters['startTime'])
        else:
            start_time = end_time

        data_end_time = get_time_offset(end_time, (meta['granularityName'], meta['granularityAmount']),
                                        + 1)
        data_start_time = get_time_offset(start_time, (meta['granularityName'], meta['granularityAmount']),
                                          - inference_window * 2)

        factor_def = parameters['seriesSets']
        # factors_data = get_timeseries(self.config, factor_def, data_start_time, data_end_time)
        factors_data = self.tsanaclient.get_timeseries(factor_def, data_start_time, data_end_time)

        target_def = [parameters['instance']['params']['target']]
        # target_data = get_timeseries(self.config, target_def, data_start_time, data_end_time)
        target_data = self.tsanaclient.get_timeseries(target_def, data_start_time, data_end_time)

        data_dir = os.path.join(self.config.model_data_dir, model_key, time_key)
        shutil.rmtree(data_dir, ignore_errors=True)
        os.makedirs(data_dir, exist_ok=True)

        for target in target_data:
            csv_file = os.path.join(data_dir, target.series_id + '.csv')
            save_csv([(tuple['timestamp'], tuple['value']) for tuple in target.value], csv_file)

        for factor in factors_data:
            csv_file = os.path.join(data_dir, factor.series_id + '.csv')
            save_csv([(tuple['timestamp'], tuple['value']) for tuple in factor.value], csv_file)

        return data_dir
