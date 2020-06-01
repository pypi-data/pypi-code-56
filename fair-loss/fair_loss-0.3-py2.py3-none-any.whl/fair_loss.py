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
        - protected_attr: :math:`(N,)`
        - input: :math:`(N, 1)`
        - target: :math:`(N, 1)`

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

    # Sum up and divide by the minimum. Then add to the regular loss
    return torch.add(loss, scores.sum() / (scores.min() + 1))


def fpr(input: torch.Tensor, target: torch.Tensor):
    """
    False Positive Rate

    Args:
        input (torch.Tensor): Predicted values
        target (torch.Tensor): Ground truth

    Shape:
        - input: :math:`(N, 1)`
        - target: :math:`(N, 1)`

    Returns:
        False Positive Rate

    Examples:
        >>> input = np.random.randint(2, size=(10, 1)).astype("float")
        >>> input = torch.tensor(input)
        >>> target = np.random.randint(2, size=(10, 1)).astype("float")
        >>> target = torch.tensor(target)
        >>> fpr(input, target)
    """
    fp = sum((input == True) & (target == False))
    tn = sum((input == False) & (target == False))
    return torch.true_divide(fp, fp + tn)


def tpr(input: torch.Tensor, target: torch.Tensor):
    """
    True Positive Rate

    Args:
        input (torch.Tensor): Predicted values
        target (torch.Tensor): Ground truth

    Shape:
        - input: :math:`(N, 1)`
        - target: :math:`(N, 1)`

    Returns:
        True Positive Rate

    Examples:
        >>> input = np.random.randint(2, size=(10, 1)).astype("float")
        >>> input = torch.tensor(input)
        >>> target = np.random.randint(2, size=(10, 1)).astype("float")
        >>> target = torch.tensor(target)
        >>> tpr(input, target)
    """
    fn = sum((input == False) & (target == True))
    tp = sum((input == True) & (target == True))
    return torch.true_divide(tp, tp + fn)


def tnr(input: torch.Tensor, target: torch.Tensor):
    """
    True Negative Rate

    Args:
        input (torch.Tensor): Predicted values
        target (torch.Tensor): Ground truth

    Shape:
        - input: :math:`(N, 1)`
        - target: :math:`(N, 1)`

    Returns:
        True Negative Rate

    Examples:
        >>> input = np.random.randint(2, size=(10, 1)).astype("float")
        >>> input = torch.tensor(input)
        >>> target = np.random.randint(2, size=(10, 1)).astype("float")
        >>> target = torch.tensor(target)
        >>> tnr(input, target)
    """
    fp = sum((input == True) & (target == False))
    tn = sum((input == False) & (target == False))
    return torch.true_divide(tn, tn + fp)


def fnr(input: torch.Tensor, target: torch.Tensor):
    """
    False Negative Rate

    Args:
        input (torch.Tensor): Predicted values
        target (torch.Tensor): Ground truth

    Shape:
        - input: :math:`(N, 1)`
        - target: :math:`(N, 1)`

    Returns:
        False Negative Rate

    Examples:
        >>> input = np.random.randint(2, size=(10, 1)).astype("float")
        >>> input = torch.tensor(input)
        >>> target = np.random.randint(2, size=(10, 1)).astype("float")
        >>> target = torch.tensor(target)
        >>> fnr(input, target)
    """
    fn = sum((input == False) & (target == True))
    tp = sum((input == True) & (target == True))
    return torch.true_divide(fn, fn + tp)


def ppv(input: torch.Tensor, target: torch.Tensor):
    """
    Positive Predicted Value

    Args:
        input (torch.Tensor): Predicted values
        target (torch.Tensor): Ground truth

    Shape:
        - input: :math:`(N, 1)`
        - target: :math:`(N, 1)`

    Returns:
        Positive Predicted Value

    Examples:
        >>> input = np.random.randint(2, size=(10, 1)).astype("float")
        >>> input = torch.tensor(input)
        >>> target = np.random.randint(2, size=(10, 1)).astype("float")
        >>> target = torch.tensor(target)
        >>> ppv(input, target)
    """
    tp = sum((input == True) & (target == True))
    fp = sum((input == True) & (target == False))
    return torch.true_divide(tp, tp + fp)


def npv(input: torch.Tensor, target: torch.Tensor):
    """
    Negative Predicted Value

    Args:
        input (torch.Tensor): Predicted values
        target (torch.Tensor): Ground truth

    Shape:
        - input: :math:`(N, 1)`
        - target: :math:`(N, 1)`

    Returns:
        Negative Predicted Value

    Examples:
        >>> input = np.random.randint(2, size=(10, 1)).astype("float")
        >>> input = torch.tensor(input)
        >>> target = np.random.randint(2, size=(10, 1)).astype("float")
        >>> target = torch.tensor(target)
        >>> npv(input, target)
    """
    tn = sum((input == False) & (target == False))
    fn = sum((input == False) & (target == True))
    return torch.true_divide(tn, tn + fn)


def accuracy(input, target):
    """
    Accuracy

    Args:
        input (torch.Tensor): Predicted values
        target (torch.Tensor): Ground truth

    Shape:
        - input: :math:`(N, 1)`
        - target: :math:`(N, 1)`

    Returns:
        Accuracy

    Examples:
        >>> input = np.random.randint(2, size=(10, 1)).astype("float")
        >>> input = torch.tensor(input)
        >>> target = np.random.randint(2, size=(10, 1)).astype("float")
        >>> target = torch.tensor(target)
        >>> accuracy(input, target)
    """
    return torch.true_divide((input == target).sum(), input.shape[0])
