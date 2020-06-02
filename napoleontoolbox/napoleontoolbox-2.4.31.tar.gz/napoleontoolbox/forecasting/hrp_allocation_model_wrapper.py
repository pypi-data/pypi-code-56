from napoleontoolbox.signal import signal_utility
from napoleontoolbox.rebalancing import allocation
import pandas as pd
import numpy as np

class HRP_Allocation_Model():
    def __init__(self):
        self.w_optim = None
        return

    def calibrate(self, X, y):
        return

    def fit(self, X_train, y_train, X_val, y_val, cutting_rate_threshold = 0.7):
        X_t = X_train.copy()
        X_t = X_t.fillna(0)
        n_step, n_asset = X_t.shape
        def filtering_process(series):
            # True if less than 50% of obs. are constant
            return series.value_counts(dropna=False).max() < cutting_rate_threshold * n_step
        assets = X_t.apply(filtering_process).values
        w_optim = np.zeros(n_asset)
        signals_returns_df = signal_utility.recompute_perf_returns(X_t.loc[:,assets],y_train)
        w_optim_assets = allocation.HRP(signals_returns_df)
        w_optim_assets = w_optim_assets.reshape(w_optim_assets.size)
        w_optim[assets] = w_optim_assets
        self.w_optim = w_optim

    def predict(self, X_test):
        data = pd.DataFrame(X_test.values * self.w_optim, columns=X_test.columns, index=X_test.index)
        X_test['signal'] = data.sum(axis=1)
        return X_test['signal'].values

    def get_features_importance(self, features_names):
        run_importances = {}
        for (name, imp) in zip(features_names, self.w_optim):
            run_importances[name] = imp
        return run_importances
