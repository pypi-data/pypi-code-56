import os
import sys
import json
import argparse
from pdb import set_trace

import pandas as pd
from tabulate import tabulate

try:
    from hpogrid.components.PandaTaskManager import PandaTaskManager
    from hpogrid.components.defaults import *
except:
    raise ImportError('Cannot import hpogrid module. Try source setupenv.sh first.')

_h_test = ''

kDefaultExtraColumns = []
kSupportedExtraColumns = ['site', 'task_time_s', 'time_s', 'taskid']


class HPOReporter():

    def __init__(self, summary=None, metric=None, mode=None):
        self.summary = summary
        self.metric = metric
        self.mode = mode

    def is_valid_data(self, data):
        if not isinstance(data, dict):
            return False
        return all(key in kHPOGridMetadataFormat for key in data)

    def get_summary(self, data, extra=[]):
        summary = []
        if not self.is_valid_data(data):
            raise RuntimeError('Invalid format for hpo result summary.')
        hparams = data['hyperparameters']
        metric = data['metric']  
        mode =  data['mode']  
        # gather results from different trials
        for index in data['result']:
            trial_result = {}
            for hp in hparams:
                trial_result[hp] = data['result'][index][hp]
            trial_result[metric] = data['result'][index][metric]
            if 'time_s' in extra:
                trial_result['time_s'] = data['result'][index]['time_total_s']
            summary.append(trial_result)
        return summary, metric, mode

    def display(self):
        if self.summary is None:
            print('WARNING: No summary to display. Action aborted.')
            return None
        df = self.to_dataframe()
        print(tabulate(df, showindex=True, headers=df.columns, tablefmt="psql",stralign='center'))

    def from_data(self, data, extra=[]):
        self.summary, self.metric, self.mode = self.get_summary(data, extra)

    def from_summary(self, summary):
        self.summary = summary

    def from_json(self, file):
        with open(file) as json_file:
            self.summary = json.load(json_file)

    def to_dataframe(self):
        if self.summary is None:
            print('WARNING: No summary found. Cannot convert summary to dataframe.')
            return None
        df = pd.DataFrame(self.summary)

        if (self.metric != None) and (self.mode != None):
            if self.mode == 'min':
                sort_ascending = True
            elif self.mode == 'max':
                sort_ascending = False
            else:
                raise RuntimeError('Invalid mode {} for the metric {}'.format(self.mode, self.metric))
            df = df.sort_values(by=[self.metric], ascending=sort_ascending).reset_index(drop=True)
        return df

    def to_json(self, file='hpo_summary.json'):
        if self.summary is None:
            print('WARNING: No summary found. Cannot convert summary to json.')
            return None
        df = self.to_dataframe()
        with open(file, 'w') as output:
            json.dump(df.to_dict(), output)

    def to_html(self, file='hpo_result.html'):
        if self.summary is None:
            print('WARNING: No summary found. Cannot convert summary to html.')
            return None
        df = self.to_dataframe()
        html_text = df.to_html()
        with open(file, 'w') as outfile:
            outfile.write(html_text)
        return html_text

    def to_parallel_coordinate_plot(self, file='hpo_result_parallel_coordinate_plot.html'):
        if self.summary is None:
            print('WARNING: No summary found. Cannot convert summary to parallel coordinate plot.')
            return None

        import hiplot as hip
        html_text = hip.Experiment.from_iterable(self.summary).to_html()
        if file is not None:
            with open(file, 'w') as outfile:
                outfile.write(html_text)
        return html_text

    def to_csv(self, file='hpo_result.csv'):
        if self.summary is None:
            print('WARNING: No summary found. Cannot convert summary to csv.')
            return None
        df = self.to_dataframe()
        csv = df.to_csv(file, encoding='utf-8')
        return csv


class HPOTaskHandle(HPOReporter):

    def __init__(self):
        super().__init__()
        self.taskmgr = PandaTaskManager()
        if len(sys.argv) > 1:
            self.run_parser()

    def get_parser(self, method=None):
        parser = argparse.ArgumentParser(description='Tool for managing HPO result',
                    formatter_class=argparse.RawDescriptionHelpFormatter)    
        parser.add_argument('proj_name', help='Name of project')
        parser.add_argument('-l','--limit', help=_h_test , type=int,
                            default=1000)
        parser.add_argument('-d', '--days', help=_h_test, type=int,
                            default=30)
        parser.add_argument('-n', '--taskname', help=_h_test)
        parser.add_argument('-r', '--range', help=_h_test)
        parser.add_argument('-e', '--extra', nargs='+',
            default=kDefaultExtraColumns)
        parser.add_argument('-j', '--to_json', action='store_true', help=_h_test)
        parser.add_argument('-t', '--to_html', action='store_true', help=_h_test)
        parser.add_argument('-c', '--to_csv', action='store_true', help=_h_test)
        parser.add_argument('-p', '--to_pcp', action='store_true', help=_h_test)
        parser.add_argument('-o', '--outname', help=_h_test, default='hpo_result')
        return parser

    def run_parser(self):
        parser = self.get_parser()
        args = parser.parse_args(sys.argv[2:])
        self.show(args)

    def show(self, args):
        params = vars(args)
        params['status'] = 'done'
        params['metadata'] = True
        proj_name = params.pop('proj_name', '')
        outname = params.pop('outname', None)
        datasets = self.taskmgr.query_tasks(**params)
        # filter tasks by jetitaskid range
        if args.range is not None:
            datasets = self.taskmgr.filter_range(datasets, args.range)
        col = ['computingsite', 'jobs_metadata', 'jeditaskid']
        datasets = self.taskmgr.filter_datasets(datasets, col)

        if args.extra:
            for extra in args.extra:
                if not extra in kSupportedExtraColumns:
                    raise ValueError('Unsupported extra column {}'.format(extra))

        self.summary, self.metric, self.mode = self.format_summary(datasets, proj_name, args.extra)
        self.display()

        if args.to_json:
            self.to_json(outname+'.json')
        if args.to_html:
            self.to_html(outname+'.html')
        if args.to_csv:
            self.to_csv(outname+'.csv')    
        if args.to_pcp:
            self.to_parallel_coordinate_plot(outname+'_parallel_coordinate_plot.html')   

    def filter_invalid_datasets(self, datasets, proj_name):
        filtered_datasets = []
        for dataset in datasets:
            metadata = self.extract_metadata(dataset)
            if not metadata:
                continue
            if not self.is_valid_data(metadata):
                continue
            if metadata['title'] != proj_name:
                continue
            filtered_datasets.append(dataset)
        if len(filtered_datasets) == 0:
            print('INFO: No results found.')
            sys.exit(1)
        metrics = set([metadata['metric'] for data in filtered_datasets])
        if not len(metrics)==1 :
            raise RuntimeError('HPO results from different tasks consist of different metrics: {}'.format(metrics))
        hparams = [metadata['hyperparameters'] for data in filtered_datasets]
        if not all(hp == hparams[0] for hp in hparams):
            raise RuntimeError('HPO results from different tasks consist of different hyperparameter space')
        return filtered_datasets

    def extract_metadata(self, dataset):
        if 'jobs_metadata' in dataset:
            keys = list(dataset['jobs_metadata'].keys())
            if keys:
                return dataset['jobs_metadata'][keys[0]]
            else:
                return None
        else:
            return None

    def format_summary(self, datasets, proj_name, extra=kDefaultExtraColumns):
        summary = []
        valid_datasets = self.filter_invalid_datasets(datasets, proj_name)

        metric =  None
        mode = None

        for data in valid_datasets:
            metadata = self.extract_metadata(data)
            task_summary, metric, mode = self.get_summary(metadata, extra)
            for ts in task_summary:
                if 'taskid' in extra:
                    ts['taskid'] = data['jeditaskid']
                if 'task_time_s' in extra:
                    ts['task_time_s'] = metadata['task_time_s']
                if 'site' in extra:
                    ts['site'] = data['computingsite']
            summary += task_summary
        return summary, metric, mode
