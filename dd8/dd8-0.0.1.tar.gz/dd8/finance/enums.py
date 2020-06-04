# -*- coding: utf-8 -*-
"""
Created on Sat Sep  7 15:16:54 2019

@author: yuanq
"""
import enum

@enum.unique
class ENUM_BINARY_METHOD(enum.Enum):
    EXCEED = 1
    WITHIN = 2

@enum.unique
class ENUM_MA_METHOD(enum.Enum):
    SMA = 1
    EMA = 2
    SMMA = 3
    LWMA = 4

@enum.unique
class ENUM_OPTION_STYLE(enum.Enum):
    EUROPEAN = 1
    AMERICAN = 2
    
@enum.unique
class ENUM_DATA_REQUEST_TYPES(enum.Enum):
    STREAMING = 1
    PER_REQUEST = 2
    HISTORICAL = 3
    INTRADAY = 4
    
@enum.unique
class ENUM_BUMP_METHOD(enum.Enum):
    ABSOLUTE = 1
    RELATIVE = 2

@enum.unique
class ENUM_FINITE_DIFFERENCE_METHOD(enum.Enum):
    FORWARD = 1
    CENTRAL = 2
    BACKWARD = 3

@enum.unique
class ENUM_CALL_PUT(enum.Enum):
    PUT = 1
    CALL = 2

@enum.unique
class ENUM_OPTION_TYPE(enum.Enum):
    EUROPEAN = 1
    AMERICAN = 2

@enum.unique
class ENUM_PRODUCT_TYPE(enum.Enum):
    VANILLA = 1
    ELSN = 2
    ELN = 3
    FCN = 4    

@enum.unique
class ENUM_ASSET_CLASS(enum.Enum):
    EQUITY = 1
    CURRENCY = 2
    INDEX = 3
    COMMODITY = 4    

@enum.unique
class ENUM_DERIVATIVE_METHOD(enum.Enum):
    CENTRAL = 1
    FORWARD = 2
    BACKWARD = 3

@enum.unique
class ENUM_FORWARD_ASSET_CLASS(enum.Enum):
    EQ = 1
    FX = 2
    IR = 3
    
@enum.unique
class ENUM_VOLATILITY_STICKINESS(enum.Enum):
    STRIKE = 1
    MONEYNESS = 2
    
@enum.unique
class ENUM_INTERPOLATION_METHOD(enum.Enum):
    LINEAR = 1
    CUBIC_SPLINE = 2
    
@enum.unique
class ENUM_COMPOUNDING_FREQUENCY(enum.Enum):
    DISCRETE = 1
    CONTINUOUS = 2
    SIMPLE = 3  
    
@enum.unique
class ENUM_DAY_COUNT_CONVENTION(enum.Enum):
    ACT_360 = 'ACT/360'
    _30_360 = '30/360'
    ACT_365 = 'ACT/365'
    _30_365 = '30/365'
    ACT_ACT = 'ACT/ACT'
    
    