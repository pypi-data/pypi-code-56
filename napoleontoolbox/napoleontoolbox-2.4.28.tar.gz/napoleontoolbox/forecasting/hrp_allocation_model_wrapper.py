from napoleontoolbox.rebalancing import allocation
from napoleontoolbox.signal import signal_utility
import pandas as pd


def recompute_perf_returns(signals_df, close_df, transac_cost=True, print_turnover = False):
    results_df = pd.concat([signals_df, close_df], axis=1).reindex(signals_df.index)
    signals_returns_df = None
    for sig in results_df.columns:
        if 'signal' in sig:
            temp_df = results_df[['close', sig]].copy()
            temp_df = temp_df.rename(columns={sig: "signal"}, errors="raise")
            freqly_df, _ = signal_utility.reconstitute_signal_perf(data=temp_df, transaction_cost=transac_cost,
                                                                   print_turnover=print_turnover)
            if signals_returns_df is None:
                signals_returns_df = freqly_df[['perf_return']].rename(columns={'perf_return': sig})
            else:
                signals_returns_df[sig] = freqly_df.perf_return
    return signals_returns_df

class HRP_Allocation_Model():
    def __init__(self):
        self.w_optim = None
        return

    def calibrate(self, X, y):
        return

    def fit(self, X_train, y_train, X_val, y_val):
        print(X_train)
        signals_returns_df = recompute_perf_returns(X_train,y_train)
        signals_returns_df = signals_returns_df.fillna(0)
        w_optim = allocation.HRP(signals_returns_df.values)
        w_optim.reshape(w_optim.size)
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
