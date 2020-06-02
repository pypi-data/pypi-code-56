"""flax.nn.Module for an auto-regressive online learner.

Todo:
    * Implement batching (efficiently! Historify gets crushed)
    * Implement projections
"""
from typing import Tuple
from typing import Union

import flax
import jax
import jax.numpy as jnp
import numpy as np

from timecast.learners._arx_history import ARXHistory
from timecast.learners.base import NewMixin
from timecast.utils.ar import historify


class ARX(NewMixin, flax.nn.Module):
    """AR online learner"""

    def apply(
        self,
        targets: np.ndarray = None,
        features: np.ndarray = None,
        history_len: int = 1,
        output_shape: Union[Tuple[int, ...], int] = 1,
        constrain: bool = True,
        batched: bool = False,
    ):
        """
        Notation
            * x = features
            * y = targets
            * H = history_len

        Estimates the following:
        
            \hat{y} = \sum_{i = 1}^{H + 1} B_i x_{t - i - 1} + a
                      \sum_{i = 1} ^ H A_i y_{t - i} + b

        Notes:
            * If batched, assume that first axis is time axis
            * If not batched, assume that features and / or targets are one
            time step and have no time or batch axis
            * Delegates much of the error checking to ARXHistory

        Args:
            targets (np.ndarray): target data
            features (np.ndarray): feature data
            output_shape (Union[Tuple[int, ...], int]): int or tuple
            describing output shape
            history_len (int): length of history
            constrain: force one parameter per for each slot in history. TODO:
            explain this better
            batched (bool): first axis is batch axis

        Returns:
            np.ndarray: result
        """

        # TODO: check that if batched, data has enough dimensions
        # TODO: check that targets / features have at least 1 dimension (i.e.,
        # not scalar)

        if history_len < 1:
            raise ValueError("Features require a history length of at least 1")

        has_targets = targets is not None and targets.ndim > 0
        has_features = features is not None and features.ndim > 0

        self.T = self.state("T", shape=())
        target_history = self.state("target_history", shape=())
        target_shape = self.state("target_shape", shape=())
        feature_history = self.state("feature_history", shape=())
        feature_shape = self.state("feature_shape", shape=())

        if self.is_initializing():
            self.T.value = 0

            if has_targets:
                target_shape.value = targets.shape[(1 if batched else 0) :]
                target_history.value = jnp.zeros((history_len,) + target_shape.value)
            if has_features:
                feature_shape.value = features.shape[(1 if batched else 0) :]
                feature_history.value = jnp.zeros((history_len,) + feature_shape.value)

        target_histories, feature_histories = None, None
        if has_targets:
            target_histories = target_history.value
            if batched:
                target_histories = historify(
                    jnp.vstack((target_histories, targets))[:-1, :], history_len=history_len
                )

        if has_features:
            feature_histories = jnp.vstack((feature_history.value, features))
            if batched:
                feature_histories = historify(feature_histories[1:, :], history_len=history_len)
            else:
                pass

        y_hat = ARXHistory(
            targets=target_histories,
            features=feature_histories,
            output_shape=output_shape,
            constrain=constrain,
            batched=batched,
        )

        # TODO: Don't duplicate the vstacks (modulo index difference for target_history)
        if not self.is_initializing():
            # Update target history with data _after_ we have made calculations
            if has_targets:
                target_history.value = jnp.vstack((target_history.value, targets))[
                    targets.shape[0] :
                ]
            if has_features:
                feature_history.value = jnp.vstack((feature_history.value, features))[
                    features.shape[0] :
                ]

            self.T.value += 1

        # If we have targets, then we need to wait one additional time step to
        # have a full target window
        return jax.lax.cond(
            self.T.value + (1 if has_targets else 0) >= history_len,
            y_hat,
            lambda x: x,
            y_hat,
            lambda x: jax.lax.stop_gradient(y_hat),
        )
