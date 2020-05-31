# SPDX-License-Identifier: GPL-3.0-only
# SPDX-FileCopyrightText: 2020 Vincent Lequertier <vi.le@autistici.org>

import torch
from typing import Callable


def FairLoss(
    protected_attr: torch.Tensor,
    loss: torch.Tensor,
    input: torch.Tensor,
    target: torch.Tensor,
    fairness_score: Callable[[torch.Tensor, torch.Tensor], torch.Tensor],
) -> torch.Tensor:
    """
    Add a fairness measure to the regular loss

    fairness_score is applied to input and target for each possible value of
    protected_attr. Then the results are sumed up and divided by the minimum

    Args:
        protected_attr (torch.Tensor): The values of the protected attribute
            for the batch
        loss (torch.Tensor): A regular loss value
        input (torch.Tensor): Predicted values
        target (torch.Tensor): Ground truth
        fairness_score (Callable[[torch.Tensor, torch.Tensor], torch.Tensor]):
            A function that takes input and target as arguments and return a
            score

    Shape:
        protected_attr: :math:`(N,)`
        input: :math:`(N, 1)`
        target: :math:`(N, 1)`

    Returns:
        The fair loss value

    Examples:
        >>> model = Model()
        >>> data = np.random.randint(5, size=(100, 5)).astype("float")
        >>> data = torch.tensor(data, requires_grad=True, dtype=torch.float)
        >>> target = np.random.randint(5, size=(100, 1)).astype("float")
        >>> target = torch.tensor(target, requires_grad=True)
        >>> input = model(data)
        >>> # The sensitive attribute is the second column
        >>> dim = 1
        >>> loss = F.mse_loss(input, target)
        >>> loss = FairLoss(data[:, dim], loss, input, target, accuracy)
    """

    # All possible values of the protected attribute
    unique = torch.unique(protected_attr)
    print(protected_attr.shape)

    scores = torch.FloatTensor(
        [
            # Apply the fairness score for each possible value
            fairness_score(
                input[torch.where(protected_attr == val)],
                target[torch.where(protected_attr == val)],
            )
            for val in unique
        ]
    )

    # Sum up and divide by the minimum. Then add to the the regular loss
    return torch.add(loss, scores.sum() / (scores.min() + 1))
