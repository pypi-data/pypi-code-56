import lightgbm as lgb
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, matthews_corrcoef, mean_squared_error
from sklearn.model_selection import KFold, StratifiedKFold
from bayes_opt import BayesianOptimization


class LightGBMwithBayesOpt():
    def __init__(self, X, y, n_fold, rangeable_params, int_params, n_tuning, target_labels=None, selective_params=None, categorical_feature=None, 
                 metrics=['mcc'], metric_larger_better=True, pred_modes=['prob_first', 'rank_first'], thresholds=None):
        self.nfold = n_fold
        self.selective_params = selective_params
        self.rangeable_params = rangeable_params
        if selective_params is not None:
            for p in list(selective_params.keys()):
                self.rangeable_params[p] = (0, len(self.selective_params[p]) - 1)
        if categorical_feature is None:
            self.categorical_feature = 'auto'
        else:
            self.categorical_feature = categorical_feature
        self.target_labels = target_labels
        if target_labels is not None:
            self.label_dist = self._value_counts_by_given_keys(y, self.target_labels)
            try:
                y1 = np.array(list(map(lambda x: int(x), y)))
            except ValueError:
                tmp = self.target_labels
                y1 = np.array([-1] * len(y))
                for i, v in enumerate(tmp):
                    y1[np.array(y) == v] = i
            self.num_y = y1
        self.X = X
        self.y = y
        if target_labels is not None:
            self.data_set = lgb.Dataset(X.loc[y1 >= 0], y1[y1 >= 0])
            self.num_class = len(self.target_labels)
        else:
            self.data_set = lgb.Dataset(X, y)
        self.int_params = set(list(int_params) + list(selective_params.keys()))
        self.parameter_tuner = None
        self.n_tuning = n_tuning
        self.parameter_perf = []
        self.best_parameter = None
        self.metric_larger_better = metric_larger_better
        self.pred_modes = pred_modes
        self.metrics = metrics
        self.thresholds = thresholds

    def _value_counts_by_given_keys(self, target, keys):
        tmp = pd.value_counts(target)
        to_in = set(keys) - set(tmp.keys())
        for k in to_in:
            tmp[k] = 0
        return tmp[keys]

    def _decode_selective_param(self, param, value):
        return self.selective_params[param][int(round(value))]

    def _do_lighgbm_cv(self, **params):
        for p in list(params.keys()):
            if p in self.int_params:
                if p in list(self.selective_params.keys()):
                    params[p] = self._decode_selective_param(p, params[p])
                else:
                    params[p] = int(round(params[p]))
        params['num_threads'] = 20
        if params['objective'] in ['multiclass', 'multiclassova']:
            params['num_class'] = self.num_class
        print(params)
        if self.target_labels is None:
            spts = KFold(self.nfold)
        else:
            spts = StratifiedKFold(self.nfold)
        result_df = []
        if self.target_labels is not None:
            nontarget_X, nontarget_y = self.X.loc[self.num_y == -1], self.num_y[self.num_y == -1]
            print(len(nontarget_y))
            X, y = self.X.loc[self.num_y >= 0].reset_index(drop=True), self.num_y[self.num_y >= 0]
        else:
            X, y = self.X, self.y
        for tr_idx, ts_idx in spts.split(X, y):
            tr_X, tr_y = X.iloc[tr_idx], np.array(y)[tr_idx]
            tr_set = lgb.Dataset(tr_X, tr_y)
            clf = self.do_train_with_given_parameter(params, tr_set)
            if len(nontarget_y) == 0:
                ts_X, ts_y = X.iloc[ts_idx], np.array(y)[ts_idx]
            else:
                ts_X = pd.concat([nontarget_X, X.iloc[ts_idx]])
                ts_y = np.concatenate([nontarget_y, np.array(y)[ts_idx]])
            result_df.append(self._do_evaluate(clf, ts_X, ts_y))
        result_df = pd.DataFrame(result_df)
        params['performance'] = np.mean(result_df.mean(1))
        print(result_df)
        print('mean: ' + str(params['performance']))
        self.parameter_perf.append(params)
        if self.metric_larger_better:
            return params['performance']
        else:
            return -params['performance']

    def _do_evaluate(self, model, X, y):
        eva = LightGBMEvalutor(model, X, self.target_labels, y)
        measures_dict = {}
        if self.target_labels is not None:
            scores_list = []
            preds_list = []
            for i, md in enumerate(self.pred_modes):
                if md in ['prob_first', 'cut_off', 'top_percentile']:
                    raw_tf = False
                elif md in ['rank_first']:
                    raw_tf = True
                scores_list.append(eva.score_predict(raw=raw_tf))
                if md in ['cut_off', 'top_percentile']:
                    thres = self.thresholds[i]
                elif md in ['prob_first', 'rank_first']:
                    thres = None
                preds_list.append(eva.label_predict(scores_list[-1], mode=md, threshold=thres))
                for mt in self.metrics:
                    measures_dict[mt + '_' + md] = eva.measure_pred_with_true(preds_list[-1], mode=mt)
        else:
            pred_values = eva.value_predict()
            measures_dict['l2'] = eva.measure_pred_with_true_value(pred_values)
        return measures_dict

    def do_parameter_tuning(self):
        self.parameter_tuner = BayesianOptimization(self._do_lighgbm_cv, self.rangeable_params)
        self.parameter_tuner.maximize(init_points=len(self.rangeable_params), n_iter=self.n_tuning)
        self.parameter_perf = pd.DataFrame(self.parameter_perf)
        if self.metric_larger_better:
            ascTF = False
        else:
            ascTF = True
        self.parameter_perf = self.parameter_perf.sort_values(by=['performance'], ascending=ascTF).reset_index(drop=True)
        tmp = self.parameter_perf.iloc[0].to_dict()
        del tmp['performance']
        self.best_parameter = tmp

    def do_train_with_given_parameter(self, params, data_set):
        return lgb.train(params, train_set=data_set, categorical_feature=self.categorical_feature, verbose_eval=False)

    def make_saveable_object(self):
        return [self.label_dist, self.parameter_perf, self.best_parameter, self.do_train_with_given_parameter(self.best_parameter, self.data_set)]


class LightGBMEvalutor():
    def __init__(self, model, X, target_labels=None, y=None, given_ids=None):
        self.target_labels = target_labels
        self.model = model
        self.X = X
        if target_labels is None:
            if y is not None:
                self.y = y
        else:
            if y is not None:
                self.y = np.array(list(y))

                ### 문자를 숫자로?!
                try:
                    if sorted(set(self.y))[0] <= 0:
                        self.new_y = self.y
                    else:
                        self.new_y = self.y
                except TypeError:
                    self.new_y = self._convert_strY_to_intY(self.y)
        if given_ids is not None:
            self.ids = given_ids

    def _convert_strY_to_intY(self, y):
        new_y = np.array([-1] * len(y))
        for i, v in enumerate(self.target_labels):
            new_y[np.array(y) == v] = i
        return new_y

    def score_predict(self, raw=False):
        if raw:
            scores = self.model.predict(self.X, raw_score=raw)
        else:
            scores = self.model.predict(self.X)
        if self.target_labels == [0, 1] or self.target_labels == ['0', '1']:
            return scores
        else:
            return pd.DataFrame(scores, columns=self.target_labels)

    def value_predict(self):
        return self.model.predict(self.X)

    def measure_pred_with_true_value(self, pred_values):
        return mean_squared_error(self.y, pred_values)

    def label_predict(self, scores, mode='prob_first', threshold=None, add_ids=False):
        """
        multiclass:
            1. 'prob_first': 각 레이블의 softmax된 score 중 최고값의 레이블 반환
            2. 'rank_first': 각 레이블의 raw score로, 동일 레이블간 최상위 percentile에 존재하는 레이블 반환
        binary-class: threshold(<= 1) 필수
            3. 'cut_off': score가 threshold 이상이라면 1, 외는 0
            4. 'top_percentile': 전체 모수 내 상위 threshold percentile까지 1, 외는 0
        """
        if mode == 'prob_first':
            labels = list(scores.idxmax(1))
        elif mode == 'rank_first':
            ranks = scores.rank(0, ascending=False)
            rank_maxes = ranks.max(0)
            labels = list((ranks / rank_maxes * 100).idxmin(1))
        elif mode == 'cut_off':
            over_tf = scores >= threshold
            labels = list(map(lambda x: int(x), over_tf))
        elif mode == 'top_percentile':
            top_n = round(threshold * len(scores))
            score_df = pd.DataFrame({'score': scores})
            score_df = score_df.sort_values(by='score', ascending=False)
            cut_off = score_df['score'].iloc[top_n]
            score_df['label'] = 0
            score_df['label'].loc[score_df['score'] >= cut_off] = 1
            labels = list(score_df.sort_index(drop=True)['label'])
        if add_ids:
            return pd.DataFrame({'svc_mgmt_num': self.ids, 'pred_label': labels})
        else:
            return labels

    def measure_pred_with_true(self, pred_list, mode='accuracy'):
        """
        accuracy = |pred_list와 real value가 동일| / 전체수
        mcc = (TP*TN - FP*FN) / sqrt((TP+FN)(TP+FP)(TN+FP)(TN+FN)) for binary-class
        """
        num_pred = self._convert_strY_to_intY(pred_list)
        if mode == 'accuracy':
            return accuracy_score(self.new_y, num_pred)
        elif mode == 'mcc':
            return matthews_corrcoef(self.new_y, num_pred)