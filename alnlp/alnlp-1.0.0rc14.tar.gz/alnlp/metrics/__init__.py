"""
A `~nlpmetrics.metric.Metric` is some quantity or quantities
that can be accumulated during training or evaluation; for example,
accuracy or F1 score.
"""

from .attachment_scores import AttachmentScores
from .average import Average
from .boolean_accuracy import BooleanAccuracy
from .bleu import BLEU
from .rouge import ROUGE
from .categorical_accuracy import CategoricalAccuracy
from .covariance import Covariance
from .entropy import Entropy
from .evalb_bracketing_scorer import (
    EvalbBracketingScorer,
    DEFAULT_EVALB_DIR,
)
from .fbeta_measure import FBetaMeasure
from .f1_measure import F1Measure
from .mean_absolute_error import MeanAbsoluteError
from .metric import Metric
from .pearson_correlation import PearsonCorrelation
from .spearman_correlation import SpearmanCorrelation
from .perplexity import Perplexity
from .sequence_accuracy import SequenceAccuracy
from .span_based_f1_measure import SpanBasedF1Measure
from .unigram_recall import UnigramRecall
from .auc import Auc
