# -----------------------
# NAME: cognite-inso-toolbox imputation module
# VERSION: 0.1
# DATE: Feb 7 2020
# Tutorial for use can be found in the notebooks folder
# Currently Supports the following methods:
# Linear Interpolation
# Matrix Factorization Interpolation
# BRITS Interpolation -> univariate & Multivariate, small sequence only
# -----------------------

import math
from abc import abstractmethod

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from autoimpute.imputations import SingleImputer
from fancyimpute import MatrixFactorization
from sklearn.preprocessing import MinMaxScaler
from torch.autograd import Variable
from torch.nn.parameter import Parameter

np.random.seed(3)


# -----------------------------------------------------------------
# The Base Imputer class. Use when constructing custom imputers
# -----------------------------------------------------------------
class BaseImputer:
    """
    Base attributes and methods for type imputer objects
    """

    def check_uniform(self, df, freq):
        new_df = df.copy()
        return new_df.resample(freq).mean()

    @abstractmethod
    def __call__(self, data: pd.DataFrame, freq: str):
        pass


# -----------------------------------------------
# UNIVARIATE TIME SERIES INTERPOLATION METHODS
# ------------------------------------------------
class Linear(BaseImputer):
    def __init__(self):
        super().__init__()

    def __call__(self, data: pd.DataFrame, freq: str):
        # check for uniformity
        new = self.check_uniform(data, freq)
        if new.isnull().values.any():
            return new.interpolate()
        else:
            return new


class TimeWeighted(BaseImputer):
    def __init__(self, **kwargs):
        super().__init__()
        self.imp = SingleImputer(strategy="default time", **kwargs)

    def __call__(self, data: pd.DataFrame, freq: str):
        # check for uniformity
        new = self.check_uniform(data, freq)
        if new.isnull().values.any():
            return self.imp.fit_transform(new)
        else:
            return new


class Mean(BaseImputer):
    def __init__(self, **kwargs):
        super().__init__()
        self.imp = SingleImputer(strategy="mean", **kwargs)

    def __call__(self, data: pd.DataFrame, freq: str):
        # check for uniformity
        new = self.check_uniform(data, freq)
        if new.isnull().values.any():
            return self.imp.fit_transform(new)
        else:
            return new


class Mode(BaseImputer):
    def __init__(self, **kwargs):
        super().__init__()
        self.imp = SingleImputer(strategy="mode", **kwargs)

    def __call__(self, data: pd.DataFrame, freq: str):
        # check for uniformity
        new = self.check_uniform(data, freq)
        if new.isnull().values.any():
            return self.imp.fit_transform(new)
        else:
            return new


class Stochastic(BaseImputer):
    def __init__(self, **kwargs):
        super().__init__()
        self.imp = SingleImputer(strategy="random", **kwargs)

    def __call__(self, data: pd.DataFrame, freq: str):
        # check for uniformity
        new = self.check_uniform(data, freq)
        if new.isnull().values.any():
            return self.imp.fit_transform(new)
        else:
            return new


class Gaussian(BaseImputer):
    def __init__(self, **kwargs):
        super().__init__()
        self.imp = SingleImputer(strategy="norm", **kwargs)

    def __call__(self, data: pd.DataFrame, freq: str):
        # check for uniformity
        new = self.check_uniform(data, freq)
        if new.isnull().values.any():
            return self.imp.fit_transform(new)
        else:
            return new


class Quadratic(BaseImputer):
    def __init__(self, **kwargs):
        super().__init__()
        self.imp = SingleImputer(
            strategy="interpolate", imp_kwgs={"interpolate": {"fill_strategy": "quadratic"}}, **kwargs
        )

    def __call__(self, data: pd.DataFrame, freq: str):
        # check for uniformity
        new = self.check_uniform(data, freq)
        if new.isnull().values.any():
            return self.imp.fit_transform(new)
        else:
            return new


class Cubic(BaseImputer):
    def __init__(self, **kwargs):
        super().__init__()
        self.imp = SingleImputer(strategy="interpolate", imp_kwgs={"interpolate": {"fill_strategy": "cubic"}}, **kwargs)

    def __call__(self, data: pd.DataFrame, freq: str):
        # check for uniformity
        new = self.check_uniform(data, freq)
        if new.isnull().values.any():
            return self.imp.fit_transform(new)
        else:
            return new


class Spline(BaseImputer):
    def __init__(self, order, **kwargs):
        super().__init__()
        self.imp = SingleImputer(
            strategy="interpolate", imp_kwgs={"interpolate": {"fill_strategy": "spline", "order": order}}, **kwargs
        )

    def __call__(self, data: pd.DataFrame, freq: str):
        # check for uniformity
        new = self.check_uniform(data, freq)
        if new.isnull().values.any():
            return self.imp.fit_transform(new)
        else:
            return new


class Polynomial(BaseImputer):
    def __init__(self, order, **kwargs):
        super().__init__()
        self.imp = SingleImputer(
            strategy="interpolate", imp_kwgs={"interpolate": {"fill_strategy": "polynomial", "order": order}}, **kwargs
        )

    def __call__(self, data: pd.DataFrame, freq: str):
        # check for uniformity
        new = self.check_uniform(data, freq)
        if new.isnull().values.any():
            return self.imp.fit_transform(new)
        else:
            return new


class MF(BaseImputer):
    """
    See docs: https://github.com/iskandr/fancyimpute. Univariate imputation Method.
    """

    def __init__(self, **kwargs):
        super().__init__()
        self.__imputer = MatrixFactorization(loss="mae", verbose=False, **kwargs)

    def __call__(self, data: pd.DataFrame, freq: str):
        new = self.check_uniform(data, freq)  # check for uniformity
        if new.isnull().values.any():
            d = new.iloc[:, 0].values.reshape(-1, 1)
            return pd.DataFrame(self.__imputer.fit_transform(d), columns=["val"])
        else:
            return new


# ------------------------
# BRITS -> Univariate
# ------------------------
class BRITS(BaseImputer):
    """
    Support for univariate imputation only.
    """

    def __init__(self, **kwargs):
        super().__init__()
        self.__imputer = BRITSModel(**kwargs)

    def __call__(self, data: pd.DataFrame, freq: str):
        new = self.check_uniform(data, freq)  # check for uniformity and correct
        if new.isnull().values.any():
            self.missing_idx = new[pd.isnull(new).any(axis=1)].index
            df, self.scalar = preprocess(new)
            data = self.scalar.inverse_transform(self.__imputer(df).reshape(new.shape[0], 1))
            return pd.DataFrame(data, index=new.index, columns=new.columns)
        else:
            return new  # data is to the correct freq return as is


class BRITSModel(nn.Module):
    def __init__(self, epochs, rnn_hid_size=108, impute_weight=0.3, opt=optim.AdamW):
        super(BRITSModel, self).__init__()
        self.rnn_hid_size = rnn_hid_size
        self.impute_weight = impute_weight
        self.base_f = BaseModel_Univariate(self.impute_weight, self.rnn_hid_size)
        self.base_b = BaseModel_Univariate(self.impute_weight, self.rnn_hid_size)
        self.optimizer = opt(self.parameters(), lr=1e-3)
        self.epochs = epochs

    def __call__(self, data):
        for epoch in range(self.epochs):
            self.train()
            run_loss = 0.0
            ret = self.run_on_batch(data, epoch)
            run_loss += ret["loss"].item()
            self.__evaluate(data)
        return self.__evaluate(data)

    def __evaluate(self, data):
        self.eval()
        evals = []
        imputations = []
        save_impute = []
        ret = self.run_on_batch(data, None)
        save_impute.append(ret["imputations"].data.cpu().numpy())
        eval_masks = ret["eval_masks"].data.cpu().numpy()
        eval_ = ret["evals"].data.cpu().numpy()
        imputation = (ret["imputations"].data.cpu().numpy()).squeeze(0)
        evals += eval_[np.where(eval_masks == 1)].tolist()
        imputations += imputation[np.where(eval_masks == 1)].tolist()
        evals = np.asarray(evals)
        imputations = np.asarray(imputations)
        save_impute = np.concatenate(save_impute, axis=0)
        return save_impute

    def forward(self, data):
        forward_pass = self.base_f(data, "forward")
        backward_pass = self.reverse(self.base_b(data, "backward"))
        return self.merge_ret(forward_pass, backward_pass)

    def merge_ret(self, ret_f, ret_b):
        loss_c = self.get_consistency_loss(ret_f["imputations"], ret_b["imputations"])
        loss = ret_f["loss"] + ret_b["loss"] + loss_c
        imputations = (ret_f["imputations"] + ret_b["imputations"]) / 2
        ret_f["loss"] = loss
        ret_f["imputations"] = imputations
        return ret_f

    def get_consistency_loss(self, pred_f, pred_b):
        return torch.abs(pred_f - pred_b).mean()

    def reverse(self, ret):
        def reverse_tensor(tensor_):
            if tensor_.dim() <= 1:
                return tensor_
            indices = range(tensor_.size()[1])[::-1]
            indices = Variable(torch.LongTensor(indices), requires_grad=False)
            return tensor_.index_select(1, indices)

        for key in ret:
            ret[key] = reverse_tensor(ret[key])

        return ret

    def run_on_batch(self, data, optimizer, epoch=None):
        ret = self.forward(data)
        if self.optimizer is not None:
            self.optimizer.zero_grad()
            ret["loss"].backward()
            self.optimizer.step()
        return ret


class TemporalDecay(nn.Module):
    def __init__(self, input_size, rnn_hid_size):
        super(TemporalDecay, self).__init__()
        self.W = Parameter(torch.Tensor(rnn_hid_size, input_size))
        self.b = Parameter(torch.Tensor(rnn_hid_size))
        self.reset_parameters()

    def reset_parameters(self):  # not sure if kaiming will make this better or not this is an old way of initialization
        stdv = 1.0 / np.sqrt(self.W.size(0))
        self.W.data.uniform_(-stdv, stdv)
        if self.b is not None:
            self.b.data.uniform_(-stdv, stdv)

    def forward(self, d):
        gamma = F.relu(F.linear(d.float(), self.W, self.b))
        gamma = torch.exp(-gamma)
        return gamma


class BaseModel_Univariate(nn.Module):
    def __init__(self, impute_weight, rnn_hid_size):
        super(BaseModel_Univariate, self).__init__()
        self.impute_weight = impute_weight
        self.rnn_hid_size = rnn_hid_size
        self.rnn_cell = nn.LSTMCell(2, self.rnn_hid_size)
        self.regression = nn.Linear(self.rnn_hid_size, 1)
        self.temp_decay = TemporalDecay(input_size=1, rnn_hid_size=self.rnn_hid_size)

    def forward(self, data, direct):
        # Start initialization
        values = (data[direct]["values"]).unsqueeze(1)
        masks = (data[direct]["masks"]).unsqueeze(1)
        deltas = data[direct]["deltas"]
        evals = data[direct]["evals"]
        eval_masks = data[direct]["eval_masks"]
        h = Variable(torch.zeros((values.size()[1], self.rnn_hid_size)))  # hidden states
        c = Variable(torch.zeros((values.size()[1], self.rnn_hid_size)))  # complement input
        x_loss = 0.0
        imputations = []
        # end initialization

        for t in range(len(values)):
            x = values[t, :].unsqueeze(1)  # xt
            m = masks[t, :].unsqueeze(1)  # mt
            d = deltas[t, :].unsqueeze(1)  # delta_t
            gamma = self.temp_decay(d)  # decays the hidden state
            h = h * gamma
            x_h = self.regression(h)  # eq 1 in paper, the regression that creates the estimated vector x_h i.e. x_hat
            x_c = m * x + (1 - m) * x_h  # equation 2 in paper
            x_loss += torch.sum(torch.abs(x - x_h) * m) / (torch.sum(m) + 1e-5)  # equation 5
            inputs = torch.cat([x_c, m], dim=1)  # inputs for the rnn part
            h, c = self.rnn_cell(inputs.float(), (h.float(), c.float()))
            imputations.append(x_c.unsqueeze(dim=1))

        imputations = torch.cat(imputations, dim=1)

        return {
            "loss": x_loss * self.impute_weight,
            "imputations": imputations,
            "evals": evals,
            "eval_masks": eval_masks,
        }

    def run_on_batch(self, data):
        ret = self.forward(data, direct="forward")
        if self.optimizer is not None:
            self.optimizer.zero_grad()
            ret["loss"].backward()
            self.optimizer.step()

        return ret


def create_deltas(masks, dir_):
    if dir_ == "backward":
        masks = masks[::-1]
    deltas = []
    for h in range(len(masks)):
        if h == 0:
            deltas.append(np.ones(1))
        else:
            deltas.append(np.ones(1) + (1 - masks[h]) * deltas[-1])

    return np.array(deltas)


def parse_df(values, masks, evals, eval_masks, direction):
    deltas = create_deltas(masks, direction)
    forwards = pd.DataFrame(values).fillna(method="ffill").fillna(0.0).values
    dic = {}
    dic["values"] = torch.from_numpy(np.nan_to_num(values))
    dic["masks"] = torch.from_numpy(masks.astype("double"))
    dic["evals"] = torch.from_numpy(np.nan_to_num(evals))
    dic["eval_masks"] = torch.from_numpy(eval_masks.astype("double"))
    dic["forwards"] = torch.from_numpy(forwards)
    dic["deltas"] = torch.from_numpy(deltas)
    return dic


def preprocess(ts, missing=False):
    data = np.array(ts.values, dtype=np.float64)  # load and correct dtype
    scaler = MinMaxScaler()  # scale
    scaler.fit(data.reshape(-1, 1))
    evals = np.squeeze(scaler.transform(data.reshape(-1, 1)), axis=1)
    shp = evals.shape
    evals = evals.reshape(-1)
    values = evals.copy()

    indices = np.argwhere(np.isnan(evals))
    values[indices] = np.nan
    # prep masks
    masks = ~np.isnan(values)
    eval_masks = (~np.isnan(values)) ^ (~np.isnan(evals))

    evals = evals.reshape(shp)
    values = values.reshape(shp)
    masks = masks.reshape(shp)
    eval_masks = eval_masks.reshape(shp)

    df = {}
    # prepare the data for both directions
    df["forward"] = parse_df(values, masks, evals, eval_masks, direction="forward")
    df["backward"] = parse_df(values[::-1], masks[::-1], evals[::-1], eval_masks[::-1], direction="backward")

    return df, scaler


# -----------------
# BRITS - Multivariate, Correlated
# ------------------
class FeatureRegression(nn.Module):
    def __init__(self, input_size):
        super(FeatureRegression, self).__init__()
        self.build(input_size)

    def build(self, input_size):
        self.W = Parameter(torch.Tensor(input_size, input_size))
        self.b = Parameter(torch.Tensor(input_size))

        m = torch.ones(input_size, input_size) - torch.eye(input_size, input_size)
        self.register_buffer("m", m)

        self.reset_parameters()

    def reset_parameters(self):
        stdv = 1.0 / math.sqrt(self.W.size(0))
        self.W.data.uniform_(-stdv, stdv)
        if self.b is not None:
            self.b.data.uniform_(-stdv, stdv)

    def forward(self, x):
        z_h = F.linear(x, self.W * Variable(self.m), self.b)
        return z_h


class TemporalDecayMultivariate(nn.Module):
    def __init__(self, input_size, output_size, diag=False):
        super(TemporalDecay, self).__init__()
        self.diag = diag
        self.W = Parameter(torch.Tensor(output_size, input_size))
        self.b = Parameter(torch.Tensor(output_size))

        if self.diag:
            assert input_size == output_size
            m = torch.eye(input_size, input_size)
            self.register_buffer("m", m)

        self.reset_parameters()

    def reset_parameters(self):
        stdv = 1.0 / math.sqrt(self.W.size(0))
        self.W.data.uniform_(-stdv, stdv)
        if self.b is not None:
            self.b.data.uniform_(-stdv, stdv)

    def forward(self, d):
        if self.diag:
            gamma = F.relu(F.linear(d, self.W * Variable(self.m), self.b))
        else:
            gamma = F.relu(F.linear(d, self.W, self.b))
        gamma = torch.exp(-gamma)
        return gamma


# class BaseModel_Multivariate(nn.Module):
#     def __init__(self, impute_weight, rnn_hid_size, siz):
#         super(BaseModel_Multivariate, self).__init__()
#         self.impute_weight = impute_weight
#         self.rnn_hid_size = rnn_hid_size
#
#         self.temp_decay_h = TemporalDecayMultivariate(input_size=siz, output_size=RNN_HID_SIZE, diag=False)
#         self.temp_decay_x = TemporalDecayMultivariate(input_size=siz, output_size=siz, diag=True)
#         self.rnn_cell = nn.LSTMCell(siz * 2, self.rnn_hid_size)
#         self.hist_reg = nn.Linear(self.rnn_hid_size, siz)
#         self.feat_reg = FeatureRegression(siz)
#
#         self.weight_combine = nn.Linear(siz * 2, siz)
#
#         self.dropout = nn.Dropout(p=0.25)
#         self.out = nn.Linear(self.rnn_hid_size, 1)
#
#     def forward(self, data, direct):
#         # Start initialization
#         values = (data[direct]["values"].values).unsqueeze(1)
#         masks = (data[direct]["masks"].values).unsqueeze(1)
#         deltas = data[direct]["deltas"].values
#         evals = data[direct]["evals"].values
#         eval_masks = data[direct]["eval_masks"].values
#
#         h = Variable(torch.zeros((values.size()[1], self.rnn_hid_size)))  # hidden states
#         c = Variable(torch.zeros((values.size()[1], self.rnn_hid_size)))  # complement input
#         x_loss = 0.0
#         imputations = []
#         # end initialization
#
#         for t in range(len(values)):
#             x = values[t, :].unsqueeze(1)  # xt
#             m = masks[t, :].unsqueeze(1)  # mt
#             d = deltas[t, :].unsqueeze(1)  # delta_t
#             gamma_h = self.temp_decay_h(d)
#             gamma_x = self.temp_decay_x(d)
#             h = h * gamma_h
#
#             x_h = self.hist_reg(h)  # eq 1 in paper, the regression that creates the estimated vector x_h i.e. x_hat
#             x_c = m * x + (1 - m) * x_h  # equation 2 in paper
#             x_loss += torch.sum(torch.abs(x - x_h) * m) / (torch.sum(m) + 1e-5)
#
#             x_c = m * x + (1 - m) * x_h
#
#             z_h = self.feat_reg(x_c)
#             x_loss += torch.sum(torch.abs(x - z_h) * m) / (torch.sum(m) + 1e-5)
#
#             alpha = self.weight_combine(torch.cat([gamma_x, m], dim=1))
#
#             c_h = alpha * z_h + (1 - alpha) * x_h
#             x_loss += torch.sum(torch.abs(x - c_h) * m) / (torch.sum(m) + 1e-5)
#
#             c_c = m * x + (1 - m) * c_h
#
#             inputs = torch.cat([c_c, m], dim=1)
#
#             h, c = self.rnn_cell(inputs, (h, c))
#
#             imputations.append(c_c.unsqueeze(dim=1))
#
#         imputations = torch.cat(imputations, dim=1)
#
#         return {
#             "loss": x_loss * self.impute_weight,
#             "imputations": imputations,
#             "evals": evals,
#             "eval_masks": eval_masks,
#         }
#
#     def run_on_batch(self, data):
#         ret = self.forward(data, direct="forward")
#         if self.optimizer is not None:
#             self.optimizer.zero_grad()
#             ret["loss"].backward()
#             self.optimizer.step()
#
#         return ret


# class BRITSModelMulti(nn.Module):
#     def __init__(self, epochs, num_ts, rnn_hid_size=108, impute_weight=0.3, opt=optim.AdamW):
#         super(BRITSModel, self).__init__()
#         self.rnn_hid_size = rnn_hid_size
#         self.impute_weight = impute_weight
#         self.base_f = BaseModel_Multivariate(self.impute_weight, self.rnn_hid_size, num_ts)
#         self.base_b = BaseModel_Multivariate(self.impute_weight, self.rnn_hid_size, num_ts)
#         self.optimizer = opt(self.parameters(), lr=1e-3)
#         self.epochs = epochs
#
#     def __call__(self, data):
#         for epoch in range(self.epochs):
#             self.train()
#             run_loss = 0.0
#             ret = self.run_on_batch(data, epoch)
#             run_loss += ret["loss"].item()
#         return self.__evaluate(data)
#
#     def __evaluate(self, data):
#         self.eval()
#         evals = []
#         imputations = []
#         save_impute = []
#         ret = self.run_on_batch(data, None)
#         save_impute.append(ret["imputations"].data.cpu().numpy())
#         eval_masks = ret["eval_masks"].data.cpu().numpy()
#         eval_ = ret["evals"].data.cpu().numpy()
#         imputation = (ret["imputations"].data.cpu().numpy()).squeeze(0)
#         evals += eval_[np.where(eval_masks == 1)].tolist()
#         imputations += imputation[np.where(eval_masks == 1)].tolist()
#         evals = np.asarray(evals)
#         imputations = np.asarray(imputations)
#         save_impute = np.concatenate(save_impute, axis=0)
#         return save_impute
#
#     def forward(self, data):
#         forward_pass = self.base_f(data, "forward")
#         backward_pass = self.reverse(self.base_b(data, "backward"))
#         return self.merge_ret(forward_pass, backward_pass)
#
#     def merge_ret(self, ret_f, ret_b):
#         loss_c = self.get_consistency_loss(ret_f["imputations"], ret_b["imputations"])
#         loss = ret_f["loss"] + ret_b["loss"] + loss_c
#         imputations = (ret_f["imputations"] + ret_b["imputations"]) / 2
#         ret_f["loss"] = loss
#         ret_f["imputations"] = imputations
#         return ret_f
#
#     def get_consistency_loss(self, pred_f, pred_b):
#         return torch.abs(pred_f - pred_b).mean()
#
#     def reverse(self, ret):
#         def reverse_tensor(tensor_):
#             if tensor_.dim() <= 1:
#                 return tensor_
#             indices = range(tensor_.size()[1])[::-1]
#             indices = Variable(torch.LongTensor(indices), requires_grad=False)
#             return tensor_.index_select(1, indices)
#
#         for key in ret:
#             ret[key] = reverse_tensor(ret[key])
#
#         return ret
#
#     def run_on_batch(self, data, optimizer, epoch=None):
#         ret = self.forward(data)
#         if self.optimizer is not None:
#             self.optimizer.zero_grad()
#             ret["loss"].backward()
#             self.optimizer.step()
#         return ret


# class BRITSMulti(BaseImputer):
#     """
#     """
#
#     def __init__(self, **kwargs):
#         super().__init__()
#         self.__imputer = BRITSModelMulti(**kwargs)
#
#     def __call__(self, data, freq):
#         new = self.check_uniform(data, freq)  # check for uniformity and correct
#         if new.isnull().values.any():
#             print("Missing Data: ", new.isnull().values.sum() * 100 / len(new), "% now interpolating ...")
#             missing_idx = new[pd.isnull(new).any(axis=1)].index
#             df, scalar = preprocess_multi(new)
#             return (
#                 pd.DataFrame(
#                     self.__imputer(df).reshape(new.shape[0], len(new.columns)), index=new.index, columns=new.columns
#                 ),
#                 scalar,
#                 missing_idx,
#                 new,
#             )
#         else:
#             return data, [], [], []  # data is to the correct freq return as is


def parse_df_multi(df, ts_name, values, masks, evals, eval_masks, direction):

    deltas = create_deltas(masks, direction)
    forwards = pd.DataFrame(values).fillna(method="ffill").fillna(0.0).values
    df["values"][ts_name] = torch.from_numpy(np.nan_to_num(values))
    df["masks"][ts_name] = torch.from_numpy(masks.astype("double"))
    df["evals"][ts_name] = torch.from_numpy(np.nan_to_num(evals))
    df["eval_masks"][ts_name] = torch.from_numpy(eval_masks.astype("double"))
    df["forwards"][ts_name] = torch.from_numpy(forwards.values)
    df["deltas"][ts_name] = torch.from_numpy(deltas)


def preprocess_multi(ts, missing=False):
    data = np.array(ts.values, dtype=np.float64)  # load and correct dtype
    scaler = MinMaxScaler()  # scale

    df_forward = {
        "values": pd.DataFrame(columns=ts.columns),
        "masks": pd.DataFrame(columns=ts.columns),
        "evals": pd.DataFrame(columns=ts.columns),
        "eval_masks": pd.DataFrame(columns=ts.columns),
        "forwards": pd.DataFrame(columns=ts.columns),
        "deltas": pd.DataFrame(columns=ts.columns),
    }

    df_backward = df_forward.copy()

    for ts_id in data.columns:
        scaler.fit(data[ts_id].reshape(-1, 1))
        evals = np.squeeze(scaler.transform(data[ts_id].reshape(-1, 1)), axis=1)
        shp = evals.shape
        evals = evals.reshape(-1)
        values = evals.copy()
        indices = np.argwhere(np.isnan(evals))
        values[indices] = np.nan
        # prep masks
        masks = ~np.isnan(values)
        eval_masks = (~np.isnan(values)) ^ (~np.isnan(evals))
        evals = evals.reshape(shp)
        values = values.reshape(shp)
        masks = masks.reshape(shp)
        eval_masks = eval_masks.reshape(shp)
        # prepare the data for both directions
        parse_df_multi(df_forward, ts_id, values, masks, evals, eval_masks, direction="forward")
        parse_df_multi(
            df_backward, ts_id, values[::-1], masks[::-1], evals[::-1], eval_masks[::-1], direction="backward"
        )

    df = {"forward": df_forward, "backward": df_backward}
    return df, scaler


# print("Missing Data: ", np.isnan(new.values.sum()) / len(new) * 100, "% now interpolating ...")
