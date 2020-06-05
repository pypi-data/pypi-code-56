""" boris.embedding

    The boris.embedding module provides trainable self-supervised
    embedding strategies.

"""

from ._base import BaseEmbedding
from ._embedding import SelfSupervisedEmbedding

__all__ = [
    'BaseEmbedding',
    'SelfSupervisedEmbedding',
]