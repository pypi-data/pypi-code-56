#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..base import Estimator, Transformer, Model, TuningEvaluator, BaseTuningModel


class KMeansModel(Model):
    CLS_NAME = 'com.alibaba.alink.pipeline.clustering.KMeansModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(KMeansModel, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setPredictionDistanceCol(self, val):
        return self._add_param('predictionDistanceCol', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class KvToColumns(Transformer):
    CLS_NAME = 'com.alibaba.alink.pipeline.dataproc.format.KvToColumns'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(KvToColumns, self).__init__(*args, **kwargs)
        pass

    def setSchemaStr(self, val):
        return self._add_param('schemaStr', val)

    def setKvCol(self, val):
        return self._add_param('kvCol', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setKvColDelimiter(self, val):
        return self._add_param('kvColDelimiter', val)

    def setKvValDelimiter(self, val):
        return self._add_param('kvValDelimiter', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class KvToCsv(Transformer):
    CLS_NAME = 'com.alibaba.alink.pipeline.dataproc.format.KvToCsv'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(KvToCsv, self).__init__(*args, **kwargs)
        pass

    def setCsvCol(self, val):
        return self._add_param('csvCol', val)

    def setSchemaStr(self, val):
        return self._add_param('schemaStr', val)

    def setKvCol(self, val):
        return self._add_param('kvCol', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setCsvFieldDelimiter(self, val):
        return self._add_param('csvFieldDelimiter', val)

    def setQuoteChar(self, val):
        return self._add_param('quoteChar', val)

    def setKvColDelimiter(self, val):
        return self._add_param('kvColDelimiter', val)

    def setKvValDelimiter(self, val):
        return self._add_param('kvValDelimiter', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class KvToJson(Transformer):
    CLS_NAME = 'com.alibaba.alink.pipeline.dataproc.format.KvToJson'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(KvToJson, self).__init__(*args, **kwargs)
        pass

    def setJsonCol(self, val):
        return self._add_param('jsonCol', val)

    def setKvCol(self, val):
        return self._add_param('kvCol', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setKvColDelimiter(self, val):
        return self._add_param('kvColDelimiter', val)

    def setKvValDelimiter(self, val):
        return self._add_param('kvValDelimiter', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class KvToVector(Transformer):
    CLS_NAME = 'com.alibaba.alink.pipeline.dataproc.format.KvToVector'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(KvToVector, self).__init__(*args, **kwargs)
        pass

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setKvCol(self, val):
        return self._add_param('kvCol', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setVectorSize(self, val):
        return self._add_param('vectorSize', val)

    def setKvColDelimiter(self, val):
        return self._add_param('kvColDelimiter', val)

    def setKvValDelimiter(self, val):
        return self._add_param('kvValDelimiter', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class LassoRegression(Estimator):
    CLS_NAME = 'com.alibaba.alink.pipeline.regression.LassoRegression'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(LassoRegression, self).__init__(*args, **kwargs)
        pass

    def setLambda(self, val):
        return self._add_param('lambda', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setOptimMethod(self, val):
        return self._add_param('optimMethod', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setWithIntercept(self, val):
        return self._add_param('withIntercept', val)

    def setMaxIter(self, val):
        return self._add_param('maxIter', val)

    def setEpsilon(self, val):
        return self._add_param('epsilon', val)

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setWeightCol(self, val):
        return self._add_param('weightCol', val)

    def setStandardization(self, val):
        return self._add_param('standardization', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class LassoRegressionModel(Model):
    CLS_NAME = 'com.alibaba.alink.pipeline.regression.LassoRegressionModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(LassoRegressionModel, self).__init__(*args, **kwargs)
        pass

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class Lda(Estimator):
    CLS_NAME = 'com.alibaba.alink.pipeline.clustering.Lda'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(Lda, self).__init__(*args, **kwargs)
        pass

    def setTopicNum(self, val):
        return self._add_param('topicNum', val)

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setAlpha(self, val):
        return self._add_param('alpha', val)

    def setBeta(self, val):
        return self._add_param('beta', val)

    def setMethod(self, val):
        return self._add_param('method', val)

    def setOnlineLearningOffset(self, val):
        return self._add_param('onlineLearningOffset', val)

    def setLearningDecay(self, val):
        return self._add_param('learningDecay', val)

    def setSubsamplingRate(self, val):
        return self._add_param('subsamplingRate', val)

    def setOptimizeDocConcentration(self, val):
        return self._add_param('optimizeDocConcentration', val)

    def setNumIter(self, val):
        return self._add_param('numIter', val)

    def setVocabSize(self, val):
        return self._add_param('vocabSize', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class LdaModel(Model):
    CLS_NAME = 'com.alibaba.alink.pipeline.clustering.LdaModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(LdaModel, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class LinearRegression(Estimator):
    CLS_NAME = 'com.alibaba.alink.pipeline.regression.LinearRegression'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(LinearRegression, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setOptimMethod(self, val):
        return self._add_param('optimMethod', val)

    def setL1(self, val):
        return self._add_param('l1', val)

    def setL2(self, val):
        return self._add_param('l2', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setWithIntercept(self, val):
        return self._add_param('withIntercept', val)

    def setMaxIter(self, val):
        return self._add_param('maxIter', val)

    def setEpsilon(self, val):
        return self._add_param('epsilon', val)

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setWeightCol(self, val):
        return self._add_param('weightCol', val)

    def setStandardization(self, val):
        return self._add_param('standardization', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class LinearRegressionModel(Model):
    CLS_NAME = 'com.alibaba.alink.pipeline.regression.LinearRegressionModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(LinearRegressionModel, self).__init__(*args, **kwargs)
        pass

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class LinearSvm(Estimator):
    CLS_NAME = 'com.alibaba.alink.pipeline.classification.LinearSvm'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(LinearSvm, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setOptimMethod(self, val):
        return self._add_param('optimMethod', val)

    def setL1(self, val):
        return self._add_param('l1', val)

    def setL2(self, val):
        return self._add_param('l2', val)

    def setWithIntercept(self, val):
        return self._add_param('withIntercept', val)

    def setMaxIter(self, val):
        return self._add_param('maxIter', val)

    def setEpsilon(self, val):
        return self._add_param('epsilon', val)

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setWeightCol(self, val):
        return self._add_param('weightCol', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setStandardization(self, val):
        return self._add_param('standardization', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)


class LinearSvmModel(Model):
    CLS_NAME = 'com.alibaba.alink.pipeline.classification.LinearSvmModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(LinearSvmModel, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class LogisticRegression(Estimator):
    CLS_NAME = 'com.alibaba.alink.pipeline.classification.LogisticRegression'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(LogisticRegression, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setOptimMethod(self, val):
        return self._add_param('optimMethod', val)

    def setL1(self, val):
        return self._add_param('l1', val)

    def setL2(self, val):
        return self._add_param('l2', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setWithIntercept(self, val):
        return self._add_param('withIntercept', val)

    def setMaxIter(self, val):
        return self._add_param('maxIter', val)

    def setEpsilon(self, val):
        return self._add_param('epsilon', val)

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setWeightCol(self, val):
        return self._add_param('weightCol', val)

    def setStandardization(self, val):
        return self._add_param('standardization', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)


class LogisticRegressionModel(Model):
    CLS_NAME = 'com.alibaba.alink.pipeline.classification.LogisticRegressionModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(LogisticRegressionModel, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class MaxAbsScaler(Estimator):
    CLS_NAME = 'com.alibaba.alink.pipeline.dataproc.MaxAbsScaler'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(MaxAbsScaler, self).__init__(*args, **kwargs)
        pass

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setOutputCols(self, val):
        return self._add_param('outputCols', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class MaxAbsScalerModel(Model):
    CLS_NAME = 'com.alibaba.alink.pipeline.dataproc.MaxAbsScalerModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(MaxAbsScalerModel, self).__init__(*args, **kwargs)
        pass

    def setOutputCols(self, val):
        return self._add_param('outputCols', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class MinMaxScaler(Estimator):
    CLS_NAME = 'com.alibaba.alink.pipeline.dataproc.MinMaxScaler'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(MinMaxScaler, self).__init__(*args, **kwargs)
        pass

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setMin(self, val):
        return self._add_param('min', val)

    def setMax(self, val):
        return self._add_param('max', val)

    def setOutputCols(self, val):
        return self._add_param('outputCols', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class MinMaxScalerModel(Model):
    CLS_NAME = 'com.alibaba.alink.pipeline.dataproc.MinMaxScalerModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(MinMaxScalerModel, self).__init__(*args, **kwargs)
        pass

    def setOutputCols(self, val):
        return self._add_param('outputCols', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class MultiStringIndexer(Estimator):
    CLS_NAME = 'com.alibaba.alink.pipeline.dataproc.MultiStringIndexer'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(MultiStringIndexer, self).__init__(*args, **kwargs)
        pass

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setStringOrderType(self, val):
        return self._add_param('stringOrderType', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setOutputCols(self, val):
        return self._add_param('outputCols', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class MultiStringIndexerModel(Model):
    CLS_NAME = 'com.alibaba.alink.pipeline.dataproc.MultiStringIndexerModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(MultiStringIndexerModel, self).__init__(*args, **kwargs)
        pass

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setOutputCols(self, val):
        return self._add_param('outputCols', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class MulticlassClassificationTuningEvaluator(TuningEvaluator):
    CLS_NAME = 'com.alibaba.alink.pipeline.tuning.MulticlassClassificationTuningEvaluator'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(MulticlassClassificationTuningEvaluator, self).__init__(*args, **kwargs)
        pass

    def setMetricName(self, val):
        return self._add_param('metricName', val)

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)


class MultilayerPerceptronClassificationModel(Model):
    CLS_NAME = 'com.alibaba.alink.pipeline.classification.MultilayerPerceptronClassificationModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(MultilayerPerceptronClassificationModel, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class MultilayerPerceptronClassifier(Estimator):
    CLS_NAME = 'com.alibaba.alink.pipeline.classification.MultilayerPerceptronClassifier'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(MultilayerPerceptronClassifier, self).__init__(*args, **kwargs)
        pass

    def setLayers(self, val):
        return self._add_param('layers', val)

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setBlockSize(self, val):
        return self._add_param('blockSize', val)

    def setInitialWeights(self, val):
        return self._add_param('initialWeights', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setMaxIter(self, val):
        return self._add_param('maxIter', val)

    def setEpsilon(self, val):
        return self._add_param('epsilon', val)

    def setL1(self, val):
        return self._add_param('l1', val)

    def setL2(self, val):
        return self._add_param('l2', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class NGram(Transformer):
    CLS_NAME = 'com.alibaba.alink.pipeline.nlp.NGram'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(NGram, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setN(self, val):
        return self._add_param('n', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class NaiveBayesTextClassifier(Estimator):
    CLS_NAME = 'com.alibaba.alink.pipeline.classification.NaiveBayesTextClassifier'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(NaiveBayesTextClassifier, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setModelType(self, val):
        return self._add_param('modelType', val)

    def setWeightCol(self, val):
        return self._add_param('weightCol', val)

    def setSmoothing(self, val):
        return self._add_param('smoothing', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class NaiveBayesTextModel(Model):
    CLS_NAME = 'com.alibaba.alink.pipeline.classification.NaiveBayesTextModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(NaiveBayesTextModel, self).__init__(*args, **kwargs)
        pass

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class OneHotEncoder(Estimator):
    CLS_NAME = 'com.alibaba.alink.pipeline.feature.OneHotEncoder'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(OneHotEncoder, self).__init__(*args, **kwargs)
        pass

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setDiscreteThresholds(self, val):
        return self._add_param('discreteThresholds', val)

    def setDiscreteThresholdsArray(self, val):
        return self._add_param('discreteThresholdsArray', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setOutputCols(self, val):
        return self._add_param('outputCols', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setEncode(self, val):
        return self._add_param('encode', val)

    def setDropLast(self, val):
        return self._add_param('dropLast', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class OneHotEncoderModel(Model):
    CLS_NAME = 'com.alibaba.alink.pipeline.feature.OneHotEncoderModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(OneHotEncoderModel, self).__init__(*args, **kwargs)
        pass

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setOutputCols(self, val):
        return self._add_param('outputCols', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setEncode(self, val):
        return self._add_param('encode', val)

    def setDropLast(self, val):
        return self._add_param('dropLast', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class _OneVsRest(Estimator):
    CLS_NAME = 'com.alibaba.alink.pipeline.classification.OneVsRest'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(_OneVsRest, self).__init__(*args, **kwargs)
        pass

    def setNumClass(self, val):
        return self._add_param('numClass', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)


class OneVsRestModel(Model):
    CLS_NAME = 'com.alibaba.alink.pipeline.classification.OneVsRestModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(OneVsRestModel, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class PCA(Estimator):
    CLS_NAME = 'com.alibaba.alink.pipeline.feature.PCA'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(PCA, self).__init__(*args, **kwargs)
        pass

    def setK(self, val):
        return self._add_param('k', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setTransformType(self, val):
        return self._add_param('transformType', val)

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setWithMean(self, val):
        return self._add_param('withMean', val)

    def setWithStd(self, val):
        return self._add_param('withStd', val)

    def setCalculationType(self, val):
        return self._add_param('calculationType', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class PCAModel(Model):
    CLS_NAME = 'com.alibaba.alink.pipeline.feature.PCAModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(PCAModel, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setTransformType(self, val):
        return self._add_param('transformType', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class QuantileDiscretizer(Estimator):
    CLS_NAME = 'com.alibaba.alink.pipeline.feature.QuantileDiscretizer'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(QuantileDiscretizer, self).__init__(*args, **kwargs)
        pass

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setNumBuckets(self, val):
        return self._add_param('numBuckets', val)

    def setNumBucketsArray(self, val):
        return self._add_param('numBucketsArray', val)

    def setLeftOpen(self, val):
        return self._add_param('leftOpen', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setOutputCols(self, val):
        return self._add_param('outputCols', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setEncode(self, val):
        return self._add_param('encode', val)

    def setDropLast(self, val):
        return self._add_param('dropLast', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class QuantileDiscretizerModel(Model):
    CLS_NAME = 'com.alibaba.alink.pipeline.feature.QuantileDiscretizerModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(QuantileDiscretizerModel, self).__init__(*args, **kwargs)
        pass

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setOutputCols(self, val):
        return self._add_param('outputCols', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setEncode(self, val):
        return self._add_param('encode', val)

    def setDropLast(self, val):
        return self._add_param('dropLast', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class RandomForestClassificationModel(Model):
    CLS_NAME = 'com.alibaba.alink.pipeline.classification.RandomForestClassificationModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(RandomForestClassificationModel, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class RandomForestClassifier(Estimator):
    CLS_NAME = 'com.alibaba.alink.pipeline.classification.RandomForestClassifier'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(RandomForestClassifier, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setFeatureSubsamplingRatio(self, val):
        return self._add_param('featureSubsamplingRatio', val)

    def setNumSubsetFeatures(self, val):
        return self._add_param('numSubsetFeatures', val)

    def setNumTrees(self, val):
        return self._add_param('numTrees', val)

    def setSubsamplingRatio(self, val):
        return self._add_param('subsamplingRatio', val)

    def setTreeType(self, val):
        return self._add_param('treeType', val)

    def setTreePartition(self, val):
        return self._add_param('treePartition', val)

    def setMaxDepth(self, val):
        return self._add_param('maxDepth', val)

    def setMinSamplesPerLeaf(self, val):
        return self._add_param('minSamplesPerLeaf', val)

    def setCreateTreeMode(self, val):
        return self._add_param('createTreeMode', val)

    def setMaxBins(self, val):
        return self._add_param('maxBins', val)

    def setMaxMemoryInMB(self, val):
        return self._add_param('maxMemoryInMB', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)

    def setCategoricalCols(self, val):
        return self._add_param('categoricalCols', val)

    def setWeightCol(self, val):
        return self._add_param('weightCol', val)

    def setMaxLeaves(self, val):
        return self._add_param('maxLeaves', val)

    def setMinSampleRatioPerChild(self, val):
        return self._add_param('minSampleRatioPerChild', val)

    def setMinInfoGain(self, val):
        return self._add_param('minInfoGain', val)


class RandomForestRegressionModel(Model):
    CLS_NAME = 'com.alibaba.alink.pipeline.regression.RandomForestRegressionModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(RandomForestRegressionModel, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class RandomForestRegressor(Estimator):
    CLS_NAME = 'com.alibaba.alink.pipeline.regression.RandomForestRegressor'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(RandomForestRegressor, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setNumSubsetFeatures(self, val):
        return self._add_param('numSubsetFeatures', val)

    def setNumTrees(self, val):
        return self._add_param('numTrees', val)

    def setSubsamplingRatio(self, val):
        return self._add_param('subsamplingRatio', val)

    def setSeed(self, val):
        return self._add_param('seed', val)

    def setMaxDepth(self, val):
        return self._add_param('maxDepth', val)

    def setMinSamplesPerLeaf(self, val):
        return self._add_param('minSamplesPerLeaf', val)

    def setCreateTreeMode(self, val):
        return self._add_param('createTreeMode', val)

    def setMaxBins(self, val):
        return self._add_param('maxBins', val)

    def setMaxMemoryInMB(self, val):
        return self._add_param('maxMemoryInMB', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)

    def setCategoricalCols(self, val):
        return self._add_param('categoricalCols', val)

    def setWeightCol(self, val):
        return self._add_param('weightCol', val)

    def setMaxLeaves(self, val):
        return self._add_param('maxLeaves', val)

    def setMinSampleRatioPerChild(self, val):
        return self._add_param('minSampleRatioPerChild', val)

    def setMinInfoGain(self, val):
        return self._add_param('minInfoGain', val)


class RegexTokenizer(Transformer):
    CLS_NAME = 'com.alibaba.alink.pipeline.nlp.RegexTokenizer'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(RegexTokenizer, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setPattern(self, val):
        return self._add_param('pattern', val)

    def setGaps(self, val):
        return self._add_param('gaps', val)

    def setMinTokenLength(self, val):
        return self._add_param('minTokenLength', val)

    def setToLowerCase(self, val):
        return self._add_param('toLowerCase', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class RegressionTuningEvaluator(TuningEvaluator):
    CLS_NAME = 'com.alibaba.alink.pipeline.tuning.RegressionTuningEvaluator'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(RegressionTuningEvaluator, self).__init__(*args, **kwargs)
        pass

    def setMetricName(self, val):
        return self._add_param('metricName', val)

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)


class RidgeRegression(Estimator):
    CLS_NAME = 'com.alibaba.alink.pipeline.regression.RidgeRegression'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(RidgeRegression, self).__init__(*args, **kwargs)
        pass

    def setLambda(self, val):
        return self._add_param('lambda', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setOptimMethod(self, val):
        return self._add_param('optimMethod', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setWithIntercept(self, val):
        return self._add_param('withIntercept', val)

    def setMaxIter(self, val):
        return self._add_param('maxIter', val)

    def setEpsilon(self, val):
        return self._add_param('epsilon', val)

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setWeightCol(self, val):
        return self._add_param('weightCol', val)

    def setStandardization(self, val):
        return self._add_param('standardization', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class RidgeRegressionModel(Model):
    CLS_NAME = 'com.alibaba.alink.pipeline.regression.RidgeRegressionModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(RidgeRegressionModel, self).__init__(*args, **kwargs)
        pass

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class Segment(Transformer):
    CLS_NAME = 'com.alibaba.alink.pipeline.nlp.Segment'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(Segment, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setUserDefinedDict(self, val):
        return self._add_param('userDefinedDict', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class Select(Transformer):
    CLS_NAME = 'com.alibaba.alink.pipeline.sql.Select'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(Select, self).__init__(*args, **kwargs)
        pass

    def setClause(self, val):
        return self._add_param('clause', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class Softmax(Estimator):
    CLS_NAME = 'com.alibaba.alink.pipeline.classification.Softmax'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(Softmax, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setOptimMethod(self, val):
        return self._add_param('optimMethod', val)

    def setL1(self, val):
        return self._add_param('l1', val)

    def setL2(self, val):
        return self._add_param('l2', val)

    def setWithIntercept(self, val):
        return self._add_param('withIntercept', val)

    def setMaxIter(self, val):
        return self._add_param('maxIter', val)

    def setEpsilon(self, val):
        return self._add_param('epsilon', val)

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setWeightCol(self, val):
        return self._add_param('weightCol', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setStandardization(self, val):
        return self._add_param('standardization', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)


class SoftmaxModel(Model):
    CLS_NAME = 'com.alibaba.alink.pipeline.classification.SoftmaxModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(SoftmaxModel, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class StandardScaler(Estimator):
    CLS_NAME = 'com.alibaba.alink.pipeline.dataproc.StandardScaler'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(StandardScaler, self).__init__(*args, **kwargs)
        pass

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setWithMean(self, val):
        return self._add_param('withMean', val)

    def setWithStd(self, val):
        return self._add_param('withStd', val)

    def setOutputCols(self, val):
        return self._add_param('outputCols', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class StandardScalerModel(Model):
    CLS_NAME = 'com.alibaba.alink.pipeline.dataproc.StandardScalerModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(StandardScalerModel, self).__init__(*args, **kwargs)
        pass

    def setOutputCols(self, val):
        return self._add_param('outputCols', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class StopWordsRemover(Transformer):
    CLS_NAME = 'com.alibaba.alink.pipeline.nlp.StopWordsRemover'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(StopWordsRemover, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setCaseSensitive(self, val):
        return self._add_param('caseSensitive', val)

    def setStopWords(self, val):
        return self._add_param('stopWords', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)

