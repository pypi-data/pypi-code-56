import torch
import torch.nn as nn

from ._score import _random_score_fn
from ._score import _coreset_score_fn

def _permutation_sample(scores):
    _, indices = torch.sort(scores, descending=True)
    return indices

def _inf(M, eps=1e-8):
    return M + eps

def _sample(n_samples, state, score_fn=_random_score_fn, device=None):
    """ Update sample state based on current state, embeddings,
        and the score function.

    Args:
        n_samples: (int) Number of samples
        state: (n_data, selected, embeddings, scores) 
            n_data: (int) size of the dataset
            selected: (torch.BoolTensor) selected samples
            embeddings: (torch.FloatTensor) TODO
            scores: (torch.FloatTensor) importance scores
        score_fn: (callable) computes new importance scores
            based on current scores and embeddings

    Returns:
        new_state: (n_data, selected, embeddings, scores)

    """

    n_data, selected, embeddings, scores = state
    n_selected = selected.sum()
    
    if n_samples <= 0:
        return state
    if n_selected >= n_data:
        return state

    if embeddings is None and scores is None:
        scores = torch.rand(n_data, device=device)
    elif not embeddings is None:
        scores = score_fn(state)
    
    scores = nn.functional.softmax(scores)
    scores[selected] = _inf(torch.max(scores))
    indices = _permutation_sample(scores)

    n_samples = min(n_data, n_selected + n_samples)
    selected[indices[n_selected:n_samples]] = True

    return (n_data, selected, embeddings, scores)


def sample(n_samples, state, strategy='random', device=None):
    """ Update sample state based on current state, embeddings,
        and the chosen strategy.

    Args:
        n_samples: (int) Number of samples
        state: (n_data, selected, embeddings, scores) 
            n_data: (int) size of the dataset
            selected: (torch.BoolTensor) selected samples
            embeddings: (torch.FloatTensor) TODO
            scores: (torch.FloatTensor) importance scores
        strategy: (str) sampling strategy from
            {random, coreset}

    Returns:
        new_state: (n_data, selected, embeddings, scores)

    """

    if strategy == 'random':
        n_data, selected, embeddings, scores = state
        state = _sample(
            n_samples, (n_data, selected, None, None), device=device)
    elif strategy == 'coreset':
        raise NotImplementedError(
            'The strategy {} is under construction'.format(strategy))
        score_fn = _coreset_score_fn
        state = _sample(n_samples, state, score_fn=score_fn, device=device)
    else:
        raise ValueError(
            'Illegal strategy: {}'.format(strategy))

    return state
