from napoleontoolbox.rebalancing import allocation
from napoleontoolbox.signal import signal_utility
import pandas as pd



class MVP_uc_Allocation_Model():
    def __init__(self):
        self.w_optim = None
        return

    def calibrate(self, X, y):
        return

    def fit(self, X_train, y_train, X_val, y_val):
        signals_returns_df = signal_utility.recompute_perf_returns(X_train,y_train)
        signals_returns_df = signals_returns_df.fillna(0)
        w_optim = allocation.MVP_uc(signals_returns_df)
        w_optim = w_optim.reshape(w_optim.size)
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
