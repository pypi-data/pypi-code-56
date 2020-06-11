import torch
import torch.nn as nn

def _random_score_fn(state):
    n_data, selected, embeddings, scores = state
    return torch.randn(n_data)

def _coreset_score_fn(state):

    n_data, selected, embeddings, scores = state
    new_scores = torch.zeros_like(selected).float()
    
    if selected.any():
        # use selected as initial centers
        labeled = selected.nonzero()
    else:
        # randomly select initial centers
        pass

    # step 1: min distances between labeled and unlabeled
    minimum_distances = None
    nearest_neighbors = None
    
    while (len(minimum_distances) < n_data):

        # step 2: add new centroid and update everything
        pass

    return new_scores

def _bitsim_score_fn(state):

    n_data, selected, embeddings, scores = state
    