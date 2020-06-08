#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..base import Estimator, Transformer, Model, TuningEvaluator, BaseTuningModel


class ALS(Estimator):
    CLS_NAME = 'com.alibaba.alink.pipeline.recommendation.ALS'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(ALS, self).__init__(*args, **kwargs)
        pass

    def setUserCol(self, val):
        return self._add_param('userCol', val)

    def setItemCol(self, val):
        return self._add_param('itemCol', val)

    def setRateCol(self, val):
        return self._add_param('rateCol', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setRank(self, val):
        return self._add_param('rank', val)

    def setLambda(self, val):
        return self._add_param('lambda', val)

    def setNonnegative(self, val):
        return self._add_param('nonnegative', val)

    def setImplicitPrefs(self, val):
        return self._add_param('implicitPrefs', val)

    def setAlpha(self, val):
        return self._add_param('alpha', val)

    def setNumBlocks(self, val):
        return self._add_param('numBlocks', val)

    def setNumIter(self, val):
        return self._add_param('numIter', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class ALSModel(Model):
    CLS_NAME = 'com.alibaba.alink.pipeline.recommendation.ALSModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(ALSModel, self).__init__(*args, **kwargs)
        pass

    def setUserCol(self, val):
        return self._add_param('userCol', val)

    def setItemCol(self, val):
        return self._add_param('itemCol', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class AftSurvivalRegression(Estimator):
    CLS_NAME = 'com.alibaba.alink.pipeline.regression.AftSurvivalRegression'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(AftSurvivalRegression, self).__init__(*args, **kwargs)
        pass

    def setCensorCol(self, val):
        return self._add_param('censorCol', val)

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setQuantileProbabilities(self, val):
        return self._add_param('quantileProbabilities', val)

    def setMaxIter(self, val):
        return self._add_param('maxIter', val)

    def setEpsilon(self, val):
        return self._add_param('epsilon', val)

    def setWithIntercept(self, val):
        return self._add_param('withIntercept', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setL1(self, val):
        return self._add_param('l1', val)

    def setL2(self, val):
        return self._add_param('l2', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class AftSurvivalRegressionModel(Model):
    CLS_NAME = 'com.alibaba.alink.pipeline.regression.AftSurvivalRegressionModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(AftSurvivalRegressionModel, self).__init__(*args, **kwargs)
        pass

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class Binarizer(Transformer):
    CLS_NAME = 'com.alibaba.alink.pipeline.feature.Binarizer'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(Binarizer, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setThreshold(self, val):
        return self._add_param('threshold', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class BinaryClassificationTuningEvaluator(TuningEvaluator):
    CLS_NAME = 'com.alibaba.alink.pipeline.tuning.BinaryClassificationTuningEvaluator'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(BinaryClassificationTuningEvaluator, self).__init__(*args, **kwargs)
        pass

    def setMetricName(self, val):
        return self._add_param('metricName', val)

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setPositiveLabelValueString(self, val):
        return self._add_param('positiveLabelValueString', val)


class BisectingKMeans(Estimator):
    CLS_NAME = 'com.alibaba.alink.pipeline.clustering.BisectingKMeans'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(BisectingKMeans, self).__init__(*args, **kwargs)
        pass

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setMinDivisibleClusterSize(self, val):
        return self._add_param('minDivisibleClusterSize', val)

    def setK(self, val):
        return self._add_param('k', val)

    def setDistanceType(self, val):
        return self._add_param('distanceType', val)

    def setMaxIter(self, val):
        return self._add_param('maxIter', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class BisectingKMeansModel(Model):
    CLS_NAME = 'com.alibaba.alink.pipeline.clustering.BisectingKMeansModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(BisectingKMeansModel, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class Bucketizer(Transformer):
    CLS_NAME = 'com.alibaba.alink.pipeline.feature.Bucketizer'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(Bucketizer, self).__init__(*args, **kwargs)
        pass

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setCutsArray(self, val):
        return self._add_param('cutsArray', val)

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


class ClusterTuningEvaluator(TuningEvaluator):
    CLS_NAME = 'com.alibaba.alink.pipeline.tuning.ClusterTuningEvaluator'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(ClusterTuningEvaluator, self).__init__(*args, **kwargs)
        pass

    def setMetricName(self, val):
        return self._add_param('metricName', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setDistanceType(self, val):
        return self._add_param('distanceType', val)


class ColumnsToCsv(Transformer):
    CLS_NAME = 'com.alibaba.alink.pipeline.dataproc.format.ColumnsToCsv'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(ColumnsToCsv, self).__init__(*args, **kwargs)
        pass

    def setCsvCol(self, val):
        return self._add_param('csvCol', val)

    def setSchemaStr(self, val):
        return self._add_param('schemaStr', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setCsvFieldDelimiter(self, val):
        return self._add_param('csvFieldDelimiter', val)

    def setQuoteChar(self, val):
        return self._add_param('quoteChar', val)

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class ColumnsToJson(Transformer):
    CLS_NAME = 'com.alibaba.alink.pipeline.dataproc.format.ColumnsToJson'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(ColumnsToJson, self).__init__(*args, **kwargs)
        pass

    def setJsonCol(self, val):
        return self._add_param('jsonCol', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class ColumnsToKv(Transformer):
    CLS_NAME = 'com.alibaba.alink.pipeline.dataproc.format.ColumnsToKv'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(ColumnsToKv, self).__init__(*args, **kwargs)
        pass

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

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class ColumnsToVector(Transformer):
    CLS_NAME = 'com.alibaba.alink.pipeline.dataproc.format.ColumnsToVector'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(ColumnsToVector, self).__init__(*args, **kwargs)
        pass

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setVectorSize(self, val):
        return self._add_param('vectorSize', val)

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class CsvToColumns(Transformer):
    CLS_NAME = 'com.alibaba.alink.pipeline.dataproc.format.CsvToColumns'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(CsvToColumns, self).__init__(*args, **kwargs)
        pass

    def setSchemaStr(self, val):
        return self._add_param('schemaStr', val)

    def setCsvCol(self, val):
        return self._add_param('csvCol', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setCsvFieldDelimiter(self, val):
        return self._add_param('csvFieldDelimiter', val)

    def setQuoteChar(self, val):
        return self._add_param('quoteChar', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class CsvToJson(Transformer):
    CLS_NAME = 'com.alibaba.alink.pipeline.dataproc.format.CsvToJson'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(CsvToJson, self).__init__(*args, **kwargs)
        pass

    def setJsonCol(self, val):
        return self._add_param('jsonCol', val)

    def setCsvCol(self, val):
        return self._add_param('csvCol', val)

    def setSchemaStr(self, val):
        return self._add_param('schemaStr', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setCsvFieldDelimiter(self, val):
        return self._add_param('csvFieldDelimiter', val)

    def setQuoteChar(self, val):
        return self._add_param('quoteChar', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class CsvToKv(Transformer):
    CLS_NAME = 'com.alibaba.alink.pipeline.dataproc.format.CsvToKv'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(CsvToKv, self).__init__(*args, **kwargs)
        pass

    def setKvCol(self, val):
        return self._add_param('kvCol', val)

    def setCsvCol(self, val):
        return self._add_param('csvCol', val)

    def setSchemaStr(self, val):
        return self._add_param('schemaStr', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setKvColDelimiter(self, val):
        return self._add_param('kvColDelimiter', val)

    def setKvValDelimiter(self, val):
        return self._add_param('kvValDelimiter', val)

    def setCsvFieldDelimiter(self, val):
        return self._add_param('csvFieldDelimiter', val)

    def setQuoteChar(self, val):
        return self._add_param('quoteChar', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class CsvToVector(Transformer):
    CLS_NAME = 'com.alibaba.alink.pipeline.dataproc.format.CsvToVector'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(CsvToVector, self).__init__(*args, **kwargs)
        pass

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setCsvCol(self, val):
        return self._add_param('csvCol', val)

    def setSchemaStr(self, val):
        return self._add_param('schemaStr', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setVectorSize(self, val):
        return self._add_param('vectorSize', val)

    def setCsvFieldDelimiter(self, val):
        return self._add_param('csvFieldDelimiter', val)

    def setQuoteChar(self, val):
        return self._add_param('quoteChar', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class DCT(Transformer):
    CLS_NAME = 'com.alibaba.alink.pipeline.feature.DCT'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(DCT, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setInverse(self, val):
        return self._add_param('inverse', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class DecisionTreeClassificationModel(Model):
    CLS_NAME = 'com.alibaba.alink.pipeline.classification.DecisionTreeClassificationModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(DecisionTreeClassificationModel, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class DecisionTreeClassifier(Estimator):
    CLS_NAME = 'com.alibaba.alink.pipeline.classification.DecisionTreeClassifier'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(DecisionTreeClassifier, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setTreeType(self, val):
        return self._add_param('treeType', val)

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


class DecisionTreeRegressionModel(Model):
    CLS_NAME = 'com.alibaba.alink.pipeline.regression.DecisionTreeRegressionModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(DecisionTreeRegressionModel, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class DecisionTreeRegressor(Estimator):
    CLS_NAME = 'com.alibaba.alink.pipeline.regression.DecisionTreeRegressor'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(DecisionTreeRegressor, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

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


class DocCountVectorizer(Estimator):
    CLS_NAME = 'com.alibaba.alink.pipeline.nlp.DocCountVectorizer'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(DocCountVectorizer, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setMaxDF(self, val):
        return self._add_param('maxDF', val)

    def setMinDF(self, val):
        return self._add_param('minDF', val)

    def setFeatureType(self, val):
        return self._add_param('featureType', val)

    def setVocabSize(self, val):
        return self._add_param('vocabSize', val)

    def setMinTF(self, val):
        return self._add_param('minTF', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)


class DocCountVectorizerModel(Model):
    CLS_NAME = 'com.alibaba.alink.pipeline.nlp.DocCountVectorizerModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(DocCountVectorizerModel, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class DocHashCountVectorizer(Estimator):
    CLS_NAME = 'com.alibaba.alink.pipeline.nlp.DocHashCountVectorizer'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(DocHashCountVectorizer, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setNumFeatures(self, val):
        return self._add_param('numFeatures', val)

    def setMinDF(self, val):
        return self._add_param('minDF', val)

    def setFeatureType(self, val):
        return self._add_param('featureType', val)

    def setMinTF(self, val):
        return self._add_param('minTF', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)


class DocHashCountVectorizerModel(Model):
    CLS_NAME = 'com.alibaba.alink.pipeline.nlp.DocHashCountVectorizerModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(DocHashCountVectorizerModel, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)


class FeatureHasher(Transformer):
    CLS_NAME = 'com.alibaba.alink.pipeline.feature.FeatureHasher'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(FeatureHasher, self).__init__(*args, **kwargs)
        pass

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setNumFeatures(self, val):
        return self._add_param('numFeatures', val)

    def setCategoricalCols(self, val):
        return self._add_param('categoricalCols', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class GaussianMixture(Estimator):
    CLS_NAME = 'com.alibaba.alink.pipeline.clustering.GaussianMixture'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(GaussianMixture, self).__init__(*args, **kwargs)
        pass

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setTol(self, val):
        return self._add_param('tol', val)

    def setK(self, val):
        return self._add_param('k', val)

    def setMaxIter(self, val):
        return self._add_param('maxIter', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class GaussianMixtureModel(Model):
    CLS_NAME = 'com.alibaba.alink.pipeline.clustering.GaussianMixtureModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(GaussianMixtureModel, self).__init__(*args, **kwargs)
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


class GbdtClassificationModel(Model):
    CLS_NAME = 'com.alibaba.alink.pipeline.classification.GbdtClassificationModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(GbdtClassificationModel, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class GbdtClassifier(Estimator):
    CLS_NAME = 'com.alibaba.alink.pipeline.classification.GbdtClassifier'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(GbdtClassifier, self).__init__(*args, **kwargs)
        pass

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setLearningRate(self, val):
        return self._add_param('learningRate', val)

    def setMinSumHessianPerLeaf(self, val):
        return self._add_param('minSumHessianPerLeaf', val)

    def setNumTrees(self, val):
        return self._add_param('numTrees', val)

    def setMinSamplesPerLeaf(self, val):
        return self._add_param('minSamplesPerLeaf', val)

    def setMaxDepth(self, val):
        return self._add_param('maxDepth', val)

    def setSubsamplingRatio(self, val):
        return self._add_param('subsamplingRatio', val)

    def setFeatureSubsamplingRatio(self, val):
        return self._add_param('featureSubsamplingRatio', val)

    def setGroupCol(self, val):
        return self._add_param('groupCol', val)

    def setMaxBins(self, val):
        return self._add_param('maxBins', val)

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

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class GbdtRegressionModel(Model):
    CLS_NAME = 'com.alibaba.alink.pipeline.regression.GbdtRegressionModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(GbdtRegressionModel, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class GbdtRegressor(Estimator):
    CLS_NAME = 'com.alibaba.alink.pipeline.regression.GbdtRegressor'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(GbdtRegressor, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setLearningRate(self, val):
        return self._add_param('learningRate', val)

    def setMinSumHessianPerLeaf(self, val):
        return self._add_param('minSumHessianPerLeaf', val)

    def setNumTrees(self, val):
        return self._add_param('numTrees', val)

    def setMinSamplesPerLeaf(self, val):
        return self._add_param('minSamplesPerLeaf', val)

    def setMaxDepth(self, val):
        return self._add_param('maxDepth', val)

    def setSubsamplingRatio(self, val):
        return self._add_param('subsamplingRatio', val)

    def setFeatureSubsamplingRatio(self, val):
        return self._add_param('featureSubsamplingRatio', val)

    def setGroupCol(self, val):
        return self._add_param('groupCol', val)

    def setMaxBins(self, val):
        return self._add_param('maxBins', val)

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


class GeneralizedLinearRegression(Estimator):
    CLS_NAME = 'com.alibaba.alink.pipeline.regression.GeneralizedLinearRegression'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(GeneralizedLinearRegression, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setFamily(self, val):
        return self._add_param('family', val)

    def setVariancePower(self, val):
        return self._add_param('variancePower', val)

    def setLink(self, val):
        return self._add_param('link', val)

    def setLinkPower(self, val):
        return self._add_param('linkPower', val)

    def setOffsetCol(self, val):
        return self._add_param('offsetCol', val)

    def setFitIntercept(self, val):
        return self._add_param('fitIntercept', val)

    def setRegParam(self, val):
        return self._add_param('regParam', val)

    def setEpsilon(self, val):
        return self._add_param('epsilon', val)

    def setLinkPredResultCol(self, val):
        return self._add_param('linkPredResultCol', val)

    def setWeightCol(self, val):
        return self._add_param('weightCol', val)

    def setMaxIter(self, val):
        return self._add_param('maxIter', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class _GeneralizedLinearRegressionModel(Model):
    CLS_NAME = 'com.alibaba.alink.pipeline.regression.GeneralizedLinearRegressionModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(_GeneralizedLinearRegressionModel, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setLinkPredResultCol(self, val):
        return self._add_param('linkPredResultCol', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class GridSearchCV(Estimator):
    CLS_NAME = 'com.alibaba.alink.pipeline.tuning.GridSearchCV'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(GridSearchCV, self).__init__(*args, **kwargs)
        pass

    def setNumFolds(self, val):
        return self._add_param('NumFolds', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class GridSearchCVModel(BaseTuningModel):
    CLS_NAME = 'com.alibaba.alink.pipeline.tuning.GridSearchCVModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(GridSearchCVModel, self).__init__(*args, **kwargs)
        pass

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class GridSearchTVSplit(Estimator):
    CLS_NAME = 'com.alibaba.alink.pipeline.tuning.GridSearchTVSplit'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(GridSearchTVSplit, self).__init__(*args, **kwargs)
        pass

    def setTrainRatio(self, val):
        return self._add_param('trainRatio', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class GridSearchTVSplitModel(BaseTuningModel):
    CLS_NAME = 'com.alibaba.alink.pipeline.tuning.GridSearchTVSplitModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(GridSearchTVSplitModel, self).__init__(*args, **kwargs)
        pass

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class Imputer(Estimator):
    CLS_NAME = 'com.alibaba.alink.pipeline.dataproc.Imputer'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(Imputer, self).__init__(*args, **kwargs)
        pass

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setStrategy(self, val):
        return self._add_param('strategy', val)

    def setFillValue(self, val):
        return self._add_param('fillValue', val)

    def setOutputCols(self, val):
        return self._add_param('outputCols', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class ImputerModel(Model):
    CLS_NAME = 'com.alibaba.alink.pipeline.dataproc.ImputerModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(ImputerModel, self).__init__(*args, **kwargs)
        pass

    def setOutputCols(self, val):
        return self._add_param('outputCols', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class IndexToString(Model):
    CLS_NAME = 'com.alibaba.alink.pipeline.dataproc.IndexToString'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(IndexToString, self).__init__(*args, **kwargs)
        pass

    def setModelName(self, val):
        return self._add_param('modelName', val)

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class IsotonicRegression(Estimator):
    CLS_NAME = 'com.alibaba.alink.pipeline.regression.IsotonicRegression'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(IsotonicRegression, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setFeatureCol(self, val):
        return self._add_param('featureCol', val)

    def setIsotonic(self, val):
        return self._add_param('isotonic', val)

    def setFeatureIndex(self, val):
        return self._add_param('featureIndex', val)

    def setWeightCol(self, val):
        return self._add_param('weightCol', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class IsotonicRegressionModel(Model):
    CLS_NAME = 'com.alibaba.alink.pipeline.regression.IsotonicRegressionModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(IsotonicRegressionModel, self).__init__(*args, **kwargs)
        pass

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class JsonToColumns(Transformer):
    CLS_NAME = 'com.alibaba.alink.pipeline.dataproc.format.JsonToColumns'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(JsonToColumns, self).__init__(*args, **kwargs)
        pass

    def setSchemaStr(self, val):
        return self._add_param('schemaStr', val)

    def setJsonCol(self, val):
        return self._add_param('jsonCol', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class JsonToCsv(Transformer):
    CLS_NAME = 'com.alibaba.alink.pipeline.dataproc.format.JsonToCsv'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(JsonToCsv, self).__init__(*args, **kwargs)
        pass

    def setCsvCol(self, val):
        return self._add_param('csvCol', val)

    def setSchemaStr(self, val):
        return self._add_param('schemaStr', val)

    def setJsonCol(self, val):
        return self._add_param('jsonCol', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setCsvFieldDelimiter(self, val):
        return self._add_param('csvFieldDelimiter', val)

    def setQuoteChar(self, val):
        return self._add_param('quoteChar', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class JsonToKv(Transformer):
    CLS_NAME = 'com.alibaba.alink.pipeline.dataproc.format.JsonToKv'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(JsonToKv, self).__init__(*args, **kwargs)
        pass

    def setKvCol(self, val):
        return self._add_param('kvCol', val)

    def setJsonCol(self, val):
        return self._add_param('jsonCol', val)

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


class JsonToVector(Transformer):
    CLS_NAME = 'com.alibaba.alink.pipeline.dataproc.format.JsonToVector'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(JsonToVector, self).__init__(*args, **kwargs)
        pass

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setJsonCol(self, val):
        return self._add_param('jsonCol', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setVectorSize(self, val):
        return self._add_param('vectorSize', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class KMeans(Estimator):
    CLS_NAME = 'com.alibaba.alink.pipeline.clustering.KMeans'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(KMeans, self).__init__(*args, **kwargs)
        pass

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setPredictionDistanceCol(self, val):
        return self._add_param('predictionDistanceCol', val)

    def setDistanceType(self, val):
        return self._add_param('distanceType', val)

    def setMaxIter(self, val):
        return self._add_param('maxIter', val)

    def setInitMode(self, val):
        return self._add_param('initMode', val)

    def setInitSteps(self, val):
        return self._add_param('initSteps', val)

    def setK(self, val):
        return self._add_param('k', val)

    def setEpsilon(self, val):
        return self._add_param('epsilon', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)

