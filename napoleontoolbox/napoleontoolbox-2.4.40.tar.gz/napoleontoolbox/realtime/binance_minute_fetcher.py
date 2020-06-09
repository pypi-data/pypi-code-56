#!/usr/bin/env python3
# coding: utf-8

from binance.websockets import BinanceSocketManager
from functools import partial
from binance.client import Client
import numpy as np
from napoleontoolbox.connector import napoleon_s3_connector
import pandas as pd
from datetime import datetime, timedelta
import boto3
from botocore.exceptions import ClientError


def pair_handling_message(fetcher, msg):
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
        if len(fetcher.minute_df)>0:
            print('persisting dataframe for the previous hour')
            fetcher.upload_last_hour_60_minutes_dataframe()
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
            new_data = [key_ts, fetcher.pair, open_dict[key_ts], high_dict[key_ts], low_dict[key_ts], close_dict[key_ts], volu_dict[key_ts]]
            print('appending one minute row '+minute_name)
            print(new_data)
            print(fetcher.minute_df.tail())
            print(len(fetcher.minute_df))
            print(fetcher.minute_df.columns)
            fetcher.minute_df.loc[len(fetcher.minute_df)] = new_data
            #fetcher.minute_df = fetcher.minute_df.append(new_data, axis = 0)
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

class NaPoleonBinanceMinutesFetcher(object):
    def __init__(self,pair, local_root_directory, binance_public, binance_secret, aws_public, aws_secret, aws_region ,bucket='napoleon-minutes'):
        self.bucket = bucket
        self.local_root_directory = local_root_directory
        self.client = Client(binance_public, binance_secret)
        self.aws_client = napoleon_s3_connector.NapoleonS3Connector(aws_public,aws_secret,region=aws_region)
        self.pair = pair
        self.minute_df = pd.DataFrame(columns=['ts','pair','open', 'high', 'low', 'close', 'volu'])
        self.pair_dict = {}
        self.pair_dict['high'] = {}
        self.pair_dict['low'] = {}
        self.pair_dict['volu'] = {}
        self.pair_dict['close'] = {}
        self.pair_dict['open'] = {}
        self.pair_dict['hour_open'] = {}

    def get_aws_last24_passed_full_hours(self):
        date_now = datetime.utcnow()
        files_to_fetch = []
        #minute_name = self.pair + '_' + date_now.strftime('%d_%b_%Y_%H_%M')
        #files_to_fetch.append(minute_name)
        d = date_now
        for i in range(24):
            d = d - timedelta(hours=1)
            minute_name = self.pair + '_' + d.strftime('%d_%b_%Y_%H')
            files_to_fetch.append(minute_name)
        aggregated_df = None
        for me_file in files_to_fetch:

            df = None
            try:
                df = self.aws_client.download_dataframe_from_csv(self.bucket, me_file)
                df = df.drop(columns=['Unnamed: 0'])
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
                    aggregated_df = df

        return aggregated_df

    def start_fetching_pair(self):
        bm = BinanceSocketManager(self.client)
        pair_callback = partial(pair_handling_message, self)
        bm.start_aggtrade_socket(self.pair, pair_callback)
        bm.start()

    def reset_minute_dataframe_to_lookback_window(self, loolback_window = 70):
        #self.minute_df = self.minute_df[0:0]
        #self.minute_df = pd.DataFrame(columns=['ts','pair','open', 'high', 'low', 'close', 'volu'])
        print('shape before reset')
        print(self.minute_df.shape)
        self.minute_df = self.minute_df[-loolback_window:]
        print('shape after reset')
        print(self.minute_df.shape)

    def upload_last_hour_60_minutes_dataframe(self):
        self.minute_df['hour_ts'] = self.minute_df['ts']-self.minute_df['ts']%3600
        self.minute_df = self.minute_df.astype({'ts': 'int32','hour_ts': 'int32'})
        if self.minute_df['hour_ts'].nunique()>1:
            print('too many hours saved together : investigate')
        hour_timestamp = self.minute_df['hour_ts'].iloc[0]
        hour_dt_object = datetime.utcfromtimestamp(hour_timestamp)
        filename = self.pair+'_'+hour_dt_object.strftime('%d_%b_%Y_%H') #str(hourr_timestamp)
        local_path = self.local_root_directory + filename
        self.minute_df.to_csv(local_path)
        self.aws_client.upload_file(self.bucket,local_path)

    def download_minute_dataframe(self, filename):
        dataframe = self.aws_client.download_dataframe_from_csv(self.bucket, filename)
        return dataframe












