#!/usr/bin/env python3
# coding: utf-8

from multiprocessing import Pool

from napoleontoolbox.file_saver import dropbox_file_saver
from napoleontoolbox.signal import signal_generator
from napoleontoolbox.connector import napoleon_connector
from napoleontoolbox.signal import signal_utility
import json

from binance.websockets import BinanceSocketManager
from functools import partial
from binance.client import Client
import numpy as np
from napoleontoolbox.connector import napoleon_s3_connector
import pandas as pd
from datetime import datetime, timedelta

import hashlib

def pair_handling_message(fetcher, msg, compute_signal=True, compute_parallel = False):
    high_dict = fetcher.pair_dict['high']
    low_dict = fetcher.pair_dict['low']
    volu_dict = fetcher.pair_dict['volu']
    close_dict = fetcher.pair_dict['close']
    open_dict = fetcher.pair_dict['open']
    hour_open_dict = fetcher.pair_dict['hour_open']

    trade_time_unix_timestamp = msg['T']/1000
    trade_time_unix_timestamp_minute = trade_time_unix_timestamp - (trade_time_unix_timestamp % 60)
    trade_time_unix_timestamp_hour = trade_time_unix_timestamp - (trade_time_unix_timestamp % 3600)

    price = float(msg['p'])

    actual_hour_open = hour_open_dict.get(trade_time_unix_timestamp_hour, np.nan)
    if np.isnan(actual_hour_open):
        # we open a new hour
        if fetcher.minute_np is not None and len(fetcher.minute_np)>0:
            print('persisting dataframe for the previous hour')
            #fetcher.upload_last_hour_60_minutes_dataframe()
            fetcher.upload_last_hour_60_minutes_signals_dataframe()
            fetcher.reset_minute_np_to_lookback_window()
    hour_open_dict[trade_time_unix_timestamp_hour] = price

    actual_open = open_dict.get(trade_time_unix_timestamp_minute, np.nan)
    if np.isnan(actual_open):
        # we open a new minute
        if len(high_dict)>1 or len(low_dict)>1 or len(volu_dict)>1 or len(close_dict)>1 or len(open_dict)>1:
            raise Exception('Trouble in paradise')
        if len(high_dict) > 0 and len(low_dict) > 0 and len(volu_dict) > 0 and len(close_dict) > 0 and len(open_dict) > 0:
            key_ts = next(iter(high_dict))
            minute_dt_object = datetime.utcfromtimestamp(key_ts)
            minute_name = fetcher.pair + '_' + minute_dt_object.strftime('%d_%b_%Y_%H_%M')
            print('appending one minute row '+minute_name)

            new_data_lst = [key_ts, open_dict[key_ts], high_dict[key_ts], low_dict[key_ts],
                            close_dict[key_ts], volu_dict[key_ts]]
            new_data = np.array(new_data_lst)

            print(new_data)
            if fetcher.minute_np is None:
                fetcher.minute_np = new_data
            else:
                fetcher.minute_np = np.vstack((fetcher.minute_np, new_data))
            if compute_signal:
                if compute_parallel:
                    fetcher.launchParallelPool()
                else:
                    fetcher.launchSequential()
            if (len(fetcher.minute_np.shape)>1 and len(fetcher.minute_np)>3):
                print('last three minutes')
                print(fetcher.minute_np[-3:,:])
            #fetcher.minute_df.loc[len(fetcher.minute_df)] = new_data
        # we clear every former minutes
        high_dict.clear()
        low_dict.clear()
        volu_dict.clear()
        close_dict.clear()
        open_dict.clear()
        open_dict[trade_time_unix_timestamp_minute] = price
    close_dict[trade_time_unix_timestamp_minute] = price
    actual_high = high_dict.get(trade_time_unix_timestamp_minute, 0)
    if price > actual_high:
        high_dict[trade_time_unix_timestamp_minute]=price
    actual_low = low_dict.get(trade_time_unix_timestamp_minute, np.inf)
    if price < actual_low:
        low_dict[trade_time_unix_timestamp_minute]=price
    actual_volu = volu_dict.get(trade_time_unix_timestamp_minute, 0)
    volu_dict[trade_time_unix_timestamp_minute] = actual_volu + float(msg['q'])

class RealTimeSignalEnsemblingParalleLauncher():
    def __init__(self, starting_date=None, running_date=None, drop_token='', dropbox_backup=True, BINANCE_PUBLIC='', BINANCE_SECRET='', AWS_PUBLIC='', AWS_SECRET='', AWS_REGION='',bucket='', local_root_directory='../data',underlying = None, pair = None, frequence='daily', selected_algo='',user='napoleon',  db_path_suffix = '_run.sqlite', list_pkl_file_suffix = 'my_list.pkl',freqly_return_pkl_filename_suffix='freqly_candels.pkl'):
        self.starting_date = starting_date
        self.running_date = running_date
        self.pair = pair
        self.BINANCE_PUBLIC = BINANCE_PUBLIC
        self.BINANCE_SECRET = BINANCE_SECRET

        self.dropbox_backup =dropbox_backup
        self.drop_token =drop_token
        self.dbx = dropbox_file_saver.NaPoleonDropboxConnector(drop_token=drop_token,dropbox_backup=dropbox_backup)

        self.AWS_PUBLIC = AWS_PUBLIC
        self.AWS_SECRET = AWS_SECRET
        self.AWS_REGION = AWS_REGION
        self.bucket = bucket

        self.client = Client(BINANCE_PUBLIC, BINANCE_SECRET)
        self.aws_client = napoleon_s3_connector.NapoleonS3Connector(AWS_PUBLIC,AWS_SECRET,region=AWS_REGION)
        self.pair = pair
        self.minute_columns = ['ts', 'open', 'high', 'low', 'close', 'volumefrom']
        self.minute_df = pd.DataFrame(columns=self.minute_columns)
        self.minute_np = None
        self.signal_np = None
        self.pair_dict = {}
        self.pair_dict['high'] = {}
        self.pair_dict['low'] = {}
        self.pair_dict['volu'] = {}
        self.pair_dict['close'] = {}
        self.pair_dict['open'] = {}
        self.pair_dict['hour_open'] = {}

        self.args = []
        self.counter = 1
        self.seed = 0
        self.local_root_directory = local_root_directory

        self.underlying = underlying
        self.list_pkl_file_suffix = list_pkl_file_suffix
        self.frequence=frequence
        self.selected_algo=selected_algo

        self.dates_stub = self.starting_date.strftime('%d_%b_%Y') + '_' + self.running_date.strftime('%d_%b_%Y')

        self.list_pkl_file_name = self.dates_stub + '_' + self.underlying + '_' + self.frequence + '_' + self.selected_algo + self.list_pkl_file_suffix
        print('selected algos')
        print(self.list_pkl_file_name)
        if self.dropbox_backup:
            self.signals_list =  self.dbx.download_pkl(self.list_pkl_file_name)
        else:
            self.signals_list = napoleon_connector.load_pickled_list(local_root_directory=self.local_root_directory,
                                                                 list_pkl_file_name=self.list_pkl_file_name)
        self.signal_mapping={}
        max_lookback_window = 0
        for me_signal in self.signals_list:
            self.args.append((me_signal))
            self.counter = self.counter + 1
            run_json_string = signal_utility.recover_to_sql_column_format(me_signal)
            params = json.loads(run_json_string)
            salty = str(int(hashlib.sha1(run_json_string.encode('utf-8')).hexdigest(), 16) % (10 ** 8))
            params = json.loads(run_json_string)
            readable_label = params['signal_type'] + str(params['trigger']) + salty
            self.signal_mapping[me_signal]=readable_label
            if params['lookback_window']>max_lookback_window:
                max_lookback_window=params['lookback_window']
        self.max_lookback_window = max_lookback_window

        self.args.sort()
        self.user = user
        self.db_path_suffix = db_path_suffix
        self.filename =  user + db_path_suffix
        self.db_path = self.local_root_directory + self.filename
        self.runs = []
        self.totalRow = 0
        self.empty_runs_to_investigate = []
        self.dbx = dropbox_file_saver.NaPoleonDropboxConnector(drop_token=drop_token,dropbox_backup=dropbox_backup)
        self.freqly_return_pkl_filename_suffix=freqly_return_pkl_filename_suffix
        self.saving_return_path = self.local_root_directory+self.underlying+self.freqly_return_pkl_filename_suffix

        self.last_minute = None


    def get_aws_last_passed_full_hours(self, nb_last_hours = 24):
        date_now = datetime.utcnow()
        files_to_fetch = []
        #minute_name = self.pair + '_' + date_now.strftime('%d_%b_%Y_%H_%M')
        #files_to_fetch.append(minute_name)
        d = date_now
        for i in range(nb_last_hours):
            d = d - timedelta(hours=1)
            minute_name = self.pair + '_' + d.strftime('%d_%b_%Y_%H')
            files_to_fetch.append(minute_name)
        aggregated_df = None
        for me_file in files_to_fetch:
            df = None
            try:
                df = self.aws_client.download_dataframe_from_csv(self.bucket, me_file)
                df = aggregated_df.df(by=['date'])
                df_test = df.pivot_table(index=['date'], aggfunc='size')
            except Exception as e:
                print(e)
                df = None
            if aggregated_df is not None:
                if df is not None:
                    print(me_file)
                    print(df.shape)
                    aggregated_df = pd.concat([aggregated_df, df])
            if aggregated_df is None:
                if df is not None:
                    print(df.shape)
                    aggregated_df = df

        return aggregated_df

    def start_fetching_pair(self):
        bm = BinanceSocketManager(self.client)
        pair_callback = partial(pair_handling_message, self)
        bm.start_aggtrade_socket(self.pair, pair_callback)
        bm.start()

    def reset_minute_np_to_lookback_window(self, loolback_window = 70):
        print('shape before reset')
        print(self.minute_np.shape)
        print(self.signal_np.shape)
        self.minute_np = self.minute_np[-loolback_window:]
        self.signal_np = self.signal_np[-loolback_window:]
        print('shape after reset')
        print(self.minute_np.shape)
        print(self.signal_np.shape)

    def update_minute_dataframe(self):
        print('updating minute df')
        if len(self.minute_np.shape)>1:
            updated_df=pd.DataFrame(data=self.minute_np, columns = self.minute_columns, index=range(len(self.minute_np)))
        else:
            updated_df=pd.DataFrame(data=self.minute_np.reshape(1,len(self.minute_np)), columns = self.minute_columns, index=[0])
        updated_df['ts'] = updated_df['ts'].astype(int)
        updated_df['ts'] = pd.to_datetime(updated_df['ts'], unit='s')
        updated_df = updated_df.sort_values(by=['ts'])
        updated_df = updated_df.rename(columns={"ts": "date"}, errors="raise")
        updated_df = updated_df.set_index(updated_df['date'])
        updated_df = updated_df.drop(columns=['date'])
        self.minute_df = updated_df
        self.last_minute = max(self.minute_df.index)

    def upload_last_hour_60_minutes_signals_dataframe(self):
        print('updating minute df')
        signal_columns = [self.signal_mapping[me_sig] for me_sig in self.signals_list]
        me_columns = self.minute_columns + signal_columns
        updated_df=pd.DataFrame(data=self.signal_np, columns = me_columns, index=range(len(self.signal_np)))
        # updated_df = updated_df.astype(
        #     {'ts': 'float64', 'open': 'float64', 'high': 'float64', 'low': 'float64', 'close': 'float64','volumefrom': 'float64'}
        #                                )
        updated_df['ts']=updated_df['ts'].astype(int)
        updated_df['hour_ts'] = updated_df['ts']-updated_df['ts']%3600
        updated_df = updated_df.astype({'hour_ts': 'int64'})
        if updated_df['hour_ts'].nunique()>1:
            print('too many hours saved together : investigate')
        hour_timestamp = updated_df['hour_ts'].max()
        hour_dt_object = datetime.utcfromtimestamp(hour_timestamp)
        filename = self.pair+'_'+hour_dt_object.strftime('%d_%b_%Y_%H') #str(hourr_timestamp)
        updated_df['ts'] = pd.to_datetime(updated_df['ts'], unit='s')
        updated_df = updated_df.sort_values(by=['ts'])
        updated_df = updated_df.rename(columns={"ts": "date"}, errors="raise")
        updated_df = updated_df.set_index(updated_df['date'])
        updated_df = updated_df.drop(columns=['date'])
        self.minute_df = updated_df
        local_path = self.local_root_directory + filename
        self.minute_df.to_csv(local_path)
        self.aws_client.upload_file(self.bucket,local_path)

    def upload_last_hour_60_minutes_dataframe(self):
        print('updating minute df')
        updated_df=pd.DataFrame(data=self.minute_np, columns = self.minute_columns, index=range(len(self.minute_np)))
        #updated_df = updated_df.astype({'ts': 'float32','open': 'float32', 'high': 'float32', 'low': 'float32', 'close': 'float32', 'volumefrom': 'float32'})
        updated_df['ts']=updated_df['ts'].astype(int)
        updated_df['hour_ts'] = updated_df['ts']-updated_df['ts']%3600
        updated_df = updated_df.astype({'hour_ts': 'int64'})
        if updated_df['hour_ts'].nunique()>1:
            print('too many hours saved together : investigate')
        hour_timestamp = updated_df['hour_ts'].max()
        hour_dt_object = datetime.utcfromtimestamp(hour_timestamp)
        filename = self.pair+'_'+hour_dt_object.strftime('%d_%b_%Y_%H') #str(hourr_timestamp)
        updated_df['ts'] = pd.to_datetime(updated_df['ts'], unit='s')
        updated_df = updated_df.sort_values(by=['ts'])
        updated_df = updated_df.rename(columns={"ts": "date"}, errors="raise")
        updated_df = updated_df.set_index(updated_df['date'])
        updated_df = updated_df.drop(columns=['date'])
        self.minute_df = updated_df
        local_path = self.local_root_directory + filename
        self.minute_df.to_csv(local_path)
        self.aws_client.upload_file(self.bucket,local_path)

    def download_minute_dataframe(self, filename):
        dataframe = self.aws_client.download_dataframe_from_csv(self.bucket, filename)
        return dataframe

    def launchParallelPool(self, use_num_cpu):
        print('launching parallel computation for alphas at '+str(self.last_minute))
        with Pool(processes=use_num_cpu) as pool:
            run_results = pool.starmap(self.runTrial, self.args)
        print('parallel computation done')
        print('results length')
        print(len(run_results))


    def launchSequential(self):
        self.update_minute_dataframe()
        print('launching sequential computation for alphas at '+str(self.last_minute))
        run_results = []
        for meArg in self.args:
            run_results.append(self.runTrial(meArg))
        print('results length')
        print(len(run_results))
        new_data_sig = np.array(run_results)
        if len(self.minute_np.shape)>1:
            new_data_sig = np.hstack((self.minute_np[-1,:].reshape(1,len(self.minute_columns)), new_data_sig.reshape(1, len(new_data_sig))))
        else:
            new_data_sig = np.hstack((self.minute_np.reshape(1,len(self.minute_columns)), new_data_sig.reshape(1, len(new_data_sig))))

        print(new_data_sig)
        if self.signal_np is None:
            self.signal_np = new_data_sig
        else:
            self.signal_np = np.vstack((self.signal_np, new_data_sig))
        if len(self.signal_np.shape)>1 and len(self.signal_np)>3:
            print('last three signals')
            print(self.signal_np[-3:])

    def runTrial(self, me_signal):
        ## idiosyncratic run itself
        run_json_string = signal_utility.recover_to_sql_column_format(me_signal)
        params = json.loads(run_json_string)
        signal_type = params['signal_type']
        normalization = params['normalization']
        trigger = params['trigger']
        transaction_costs = params['transaction_costs']
        if normalization and not signal_generator.is_signal_continuum(signal_type):
            return
        lookback_window = params['lookback_window']
        if lookback_window>self.minute_df.shape[0]:
            return np.nan
        freqly = self.minute_df.iloc[-lookback_window:,:].copy()
        signal_generation_method_to_call = getattr(signal_generator, signal_type)
        last_generated_signal = signal_utility.compute_last_signal(freqly, lookback_window,
                                                                   lambda x: signal_generation_method_to_call(
                                                                       data=x, **params))
        return last_generated_signal