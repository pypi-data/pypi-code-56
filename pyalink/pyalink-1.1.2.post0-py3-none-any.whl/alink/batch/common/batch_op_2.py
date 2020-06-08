#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..base import BatchOperator, BaseSinkBatchOp


class GbdtTrainBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.classification.GbdtTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(GbdtTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setAlgoType(self, val):
        return self._add_param('algoType', val)

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


class GlmEvaluationBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.regression.GlmEvaluationBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(GlmEvaluationBatchOp, self).__init__(*args, **kwargs)
        pass

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

    def setWeightCol(self, val):
        return self._add_param('weightCol', val)

    def setMaxIter(self, val):
        return self._add_param('maxIter', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class GlmPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.regression.GlmPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(GlmPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setLinkPredResultCol(self, val):
        return self._add_param('linkPredResultCol', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class GlmTrainBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.regression.GlmTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(GlmTrainBatchOp, self).__init__(*args, **kwargs)
        pass

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

    def setWeightCol(self, val):
        return self._add_param('weightCol', val)

    def setMaxIter(self, val):
        return self._add_param('maxIter', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class GmmPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.clustering.GmmPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(GmmPredictBatchOp, self).__init__(*args, **kwargs)
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


class GmmTrainBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.clustering.GmmTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(GmmTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setTol(self, val):
        return self._add_param('tol', val)

    def setK(self, val):
        return self._add_param('k', val)

    def setMaxIter(self, val):
        return self._add_param('maxIter', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class GroupByBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.sql.GroupByBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(GroupByBatchOp, self).__init__(*args, **kwargs)
        pass

    def setGroupByPredicate(self, val):
        return self._add_param('groupByPredicate', val)

    def setSelectClause(self, val):
        return self._add_param('selectClause', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class HiveSinkBatchOp(BaseSinkBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.sink.HiveSinkBatchOp'
    OP_TYPE = 'SINK'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(HiveSinkBatchOp, self).__init__(*args, **kwargs)
        pass

    def setHiveConfDir(self, val):
        return self._add_param('hiveConfDir', val)

    def setHiveVersion(self, val):
        return self._add_param('hiveVersion', val)

    def setDbName(self, val):
        return self._add_param('dbName', val)

    def setOutputTableName(self, val):
        return self._add_param('outputTableName', val)

    def setPartition(self, val):
        return self._add_param('partition', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class HiveSourceBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.source.HiveSourceBatchOp'
    OP_TYPE = 'SOURCE'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(HiveSourceBatchOp, self).__init__(*args, **kwargs)
        pass

    def setHiveConfDir(self, val):
        return self._add_param('hiveConfDir', val)

    def setHiveVersion(self, val):
        return self._add_param('hiveVersion', val)

    def setDbName(self, val):
        return self._add_param('dbName', val)

    def setInputTableName(self, val):
        return self._add_param('inputTableName', val)

    def setPartitions(self, val):
        return self._add_param('partitions', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class ImputerPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.ImputerPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(ImputerPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setOutputCols(self, val):
        return self._add_param('outputCols', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class ImputerTrainBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.ImputerTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(ImputerTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setStrategy(self, val):
        return self._add_param('strategy', val)

    def setFillValue(self, val):
        return self._add_param('fillValue', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class InMemorySourceBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.executor.python.util.InMemorySourceBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(InMemorySourceBatchOp, self).__init__(*args, **kwargs)
        pass

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class IndexToStringPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.IndexToStringPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(IndexToStringPredictBatchOp, self).__init__(*args, **kwargs)
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


class IntersectAllBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.sql.IntersectAllBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(IntersectAllBatchOp, self).__init__(*args, **kwargs)
        pass

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class IntersectBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.sql.IntersectBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(IntersectBatchOp, self).__init__(*args, **kwargs)
        pass

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class IsotonicRegPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.regression.IsotonicRegPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(IsotonicRegPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class IsotonicRegTrainBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.regression.IsotonicRegTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(IsotonicRegTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

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


class JoinBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.sql.JoinBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(JoinBatchOp, self).__init__(*args, **kwargs)
        pass

    def setJoinPredicate(self, val):
        return self._add_param('joinPredicate', val)

    def setSelectClause(self, val):
        return self._add_param('selectClause', val)

    def setType(self, val):
        return self._add_param('type', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class JsonToColumnsBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.format.JsonToColumnsBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(JsonToColumnsBatchOp, self).__init__(*args, **kwargs)
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


class JsonToCsvBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.format.JsonToCsvBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(JsonToCsvBatchOp, self).__init__(*args, **kwargs)
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


class JsonToKvBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.format.JsonToKvBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(JsonToKvBatchOp, self).__init__(*args, **kwargs)
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


class JsonToTripleBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.format.JsonToTripleBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(JsonToTripleBatchOp, self).__init__(*args, **kwargs)
        pass

    def setTripleColValSchemaStr(self, val):
        return self._add_param('tripleColValSchemaStr', val)

    def setJsonCol(self, val):
        return self._add_param('jsonCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class JsonToVectorBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.format.JsonToVectorBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(JsonToVectorBatchOp, self).__init__(*args, **kwargs)
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


class JsonValueBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.JsonValueBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(JsonValueBatchOp, self).__init__(*args, **kwargs)
        pass

    def setJsonPath(self, val):
        return self._add_param('jsonPath', val)

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setOutputCols(self, val):
        return self._add_param('outputCols', val)

    def setSkipFailed(self, val):
        return self._add_param('skipFailed', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class KMeansPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.clustering.KMeansPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(KMeansPredictBatchOp, self).__init__(*args, **kwargs)
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


class KMeansTrainBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.clustering.KMeansTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(KMeansTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setDistanceType(self, val):
        return self._add_param('distanceType', val)

    def setMaxIter(self, val):
        return self._add_param('maxIter', val)

    def setInitMode(self, val):
        return self._add_param('initMode', val)

    def setInitSteps(self, val):
        return self._add_param('initSteps', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)

    def setK(self, val):
        return self._add_param('k', val)

    def setEpsilon(self, val):
        return self._add_param('epsilon', val)


class KvToColumnsBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.format.KvToColumnsBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(KvToColumnsBatchOp, self).__init__(*args, **kwargs)
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


class KvToCsvBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.format.KvToCsvBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(KvToCsvBatchOp, self).__init__(*args, **kwargs)
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


class KvToJsonBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.format.KvToJsonBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(KvToJsonBatchOp, self).__init__(*args, **kwargs)
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


class KvToTripleBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.format.KvToTripleBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(KvToTripleBatchOp, self).__init__(*args, **kwargs)
        pass

    def setTripleColValSchemaStr(self, val):
        return self._add_param('tripleColValSchemaStr', val)

    def setKvCol(self, val):
        return self._add_param('kvCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setKvColDelimiter(self, val):
        return self._add_param('kvColDelimiter', val)

    def setKvValDelimiter(self, val):
        return self._add_param('kvValDelimiter', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class KvToVectorBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.format.KvToVectorBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(KvToVectorBatchOp, self).__init__(*args, **kwargs)
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


class LassoRegPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.regression.LassoRegPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(LassoRegPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class LassoRegTrainBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.regression.LassoRegTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(LassoRegTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setLambda(self, val):
        return self._add_param('lambda', val)

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setOptimMethod(self, val):
        return self._add_param('optimMethod', val)

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


class LdaPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.clustering.LdaPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(LdaPredictBatchOp, self).__init__(*args, **kwargs)
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


class LdaTrainBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.clustering.LdaTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(LdaTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setTopicNum(self, val):
        return self._add_param('topicNum', val)

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

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

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class LeftOuterJoinBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.sql.LeftOuterJoinBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(LeftOuterJoinBatchOp, self).__init__(*args, **kwargs)
        pass

    def setJoinPredicate(self, val):
        return self._add_param('joinPredicate', val)

    def setSelectClause(self, val):
        return self._add_param('selectClause', val)

    def setType(self, val):
        return self._add_param('type', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class LibSvmSinkBatchOp(BaseSinkBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.sink.LibSvmSinkBatchOp'
    OP_TYPE = 'SINK'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(LibSvmSinkBatchOp, self).__init__(*args, **kwargs)
        pass

    def setFilePath(self, val):
        return self._add_param('filePath', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class LibSvmSourceBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.source.LibSvmSourceBatchOp'
    OP_TYPE = 'SOURCE'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(LibSvmSourceBatchOp, self).__init__(*args, **kwargs)
        pass

    def setFilePath(self, val):
        return self._add_param('filePath', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class LinearRegPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.regression.LinearRegPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(LinearRegPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class LinearRegTrainBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.regression.LinearRegTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(LinearRegTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

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


class LinearSvmPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.classification.LinearSvmPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(LinearSvmPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)


class LinearSvmTrainBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.classification.LinearSvmTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(LinearSvmTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

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


class LogisticRegressionPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.classification.LogisticRegressionPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(LogisticRegressionPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)


class LogisticRegressionTrainBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.classification.LogisticRegressionTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(LogisticRegressionTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

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


class MaxAbsScalerPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.MaxAbsScalerPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(MaxAbsScalerPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setOutputCols(self, val):
        return self._add_param('outputCols', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class MaxAbsScalerTrainBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.MaxAbsScalerTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(MaxAbsScalerTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class MinMaxScalerPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.MinMaxScalerPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(MinMaxScalerPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setOutputCols(self, val):
        return self._add_param('outputCols', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class MinMaxScalerTrainBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.MinMaxScalerTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(MinMaxScalerTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setMin(self, val):
        return self._add_param('min', val)

    def setMax(self, val):
        return self._add_param('max', val)

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class MinusAllBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.sql.MinusAllBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(MinusAllBatchOp, self).__init__(*args, **kwargs)
        pass

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)


class MinusBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.sql.MinusBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(MinusBatchOp, self).__init__(*args, **kwargs)
        pass

    def setMLEnvironmentId(self, val):
        return self._add_param('MLEnvironmentId', val)

