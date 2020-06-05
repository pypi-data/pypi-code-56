# Copyright 2019 AstroLab Software
# Author: Julien Peloton
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from pyspark.sql import SparkSession
import pyspark.sql.functions as F

from fink_science.simple_snn.processor import snnscore
from fink_science.random_forest_snia.classifier import concat_col

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

sns.set_context('talk')

spark = SparkSession.builder.getOrCreate()

spark.sparkContext.setLogLevel('WARN')

fn = '/Users/julien/Documents/workspace/myrepos/des2ztf/DESSMALL4'

df = spark.read.parquet(fn)

df = df.sample(fraction=0.01)

# df.show()
#
# spark.sparkContext.stop()

# df = df.sample(fraction=0.001)

# Required alert columns
what = [
    'jd', 'fid', 'magpsf', 'sigmapsf',
    'magnr', 'sigmagnr', 'magzpsci', 'isdiffpos'
]

# Use for creating temp name
prefix = 'c'
what_prefix = [prefix + i for i in what]

# Append temp columns with historical + current measurements
for colname in what:
    df = concat_col(df, colname, prefix=prefix)

# Perform the fit + classification.
# Note we can omit the model_path argument, and in that case the
# default model `data/models/default-model.obj` will be used.
rfscore_args = [F.col(i) for i in ['objectId', 'publisher'] + what_prefix]

df = df.withColumn(snnscore.__name__, snnscore(*rfscore_args))

# Drop temp columns
df = df.drop(*what_prefix)

df = df.selectExpr("publisher as input", "snnscore as target")
df.select(['input', 'target']).show()

targets = np.array([i[0] for i in df.select('target').collect()])
inputs = np.array([i[0] for i in df.select('input').collect()])

inputs = np.array([0 if 'Ia' in i else 1 for i in inputs])
print('input length', len(inputs))
print('acc', sum(np.array(targets) == np.array(inputs)) / len(inputs))
mask0 = np.where(inputs == 0)[0]
print('acc - 0', sum(np.array([targets[i] for i in mask0]) == np.array([inputs[i] for i in mask0])) / len(mask0))
mask1 = np.where(inputs == 1)[0]
print('acc - 1', sum(np.array([targets[i] for i in mask1]) == np.array([inputs[i] for i in mask1])) / len(mask1))
