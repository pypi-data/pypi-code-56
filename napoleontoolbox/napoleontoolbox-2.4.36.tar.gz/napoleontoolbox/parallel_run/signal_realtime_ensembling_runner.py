#!/usr/bin/env python
# coding: utf-8

from abc import ABC, abstractmethod

import pandas as pd

from napoleontoolbox.file_saver import dropbox_file_saver
from napoleontoolbox.signal import signal_generator
from napoleontoolbox.connector import napoleon_connector
from napoleontoolbox.signal import signal_utility
from napoleontoolbox.parallel_run import signal_result_analyzer
from napoleontoolbox.parallel_run import launcher_utility
import json

from pathlib import Path

class AbstractRunner(ABC):
    def __init__(self, starting_date = None, running_date = None, drop_token=None, dropbox_backup = True, underlying = None, frequence='daily',local_root_directory='../data/'):
        super().__init__()
        self.starting_date = starting_date
        self.running_date = running_date
        self.underlying = underlying
        self.frequence=frequence
        self.local_root_directory=local_root_directory
        self.dropbox_backup = dropbox_backup
        self.dbx = dropbox_file_saver.NaPoleonDropboxConnector(drop_token=drop_token,dropbox_backup=dropbox_backup)
        self.running_date = running_date
        self.starting_date = starting_date

    @abstractmethod
    def runTrial(self, saver, serialized_signal):
        pass


class RealTimeEnsemblingSignalRunner(AbstractRunner):

    def runTrial(self, saver, me_signal):

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
        signal_generation_method_to_call = getattr(signal_generator, signal_type)
        last_generated_signal = signal_utility.compute_last_signal(saver.freqly_df, lookback_window,
                                                                   lambda x: signal_generation_method_to_call(
                                                                       data=x, **params))
        print('last_generated_signal')
        print(last_generated_signal)
        return last_generated_signal









