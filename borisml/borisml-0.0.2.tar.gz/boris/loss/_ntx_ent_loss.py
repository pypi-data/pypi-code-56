""" Contrastive Loss Functions """

import torch
import numpy as np

class NTXentLoss(torch.nn.Module):
    """ Contrastive Cross Entropy Loss """

    def __init__(self, temperature=0.5, use_cosine_similarity=True):
        """ Constructor

        Args:
            temperature: (float) Scale logits
            use_cosine_similarity: (bool) Use cosine similarity over L2

        """
        super(NTXentLoss, self).__init__()
        self.temperature = temperature
        self.similarity_function = self._get_similarity_function(use_cosine_similarity)
        self.cross_entropy = torch.nn.CrossEntropyLoss(reduction="sum")
        self.correlated_mask = None

    def _get_similarity_function(self, use_cosine_similarity):
        if use_cosine_similarity:
            self._cosine_similarity = torch.nn.CosineSimilarity(dim=-1)
            return self._cosine_simililarity
        else:
            return self._dot_simililarity

    def _torch_get_correlated_mask(self, batch_size):
        diag = torch.eye(2 * batch_size)
        diag[batch_size:, :batch_size] += torch.eye(batch_size)
        diag[:batch_size, batch_size:] += torch.eye(batch_size)
        mask = (1 - diag).type(torch.bool)
        return mask

    def _get_correlated_mask(self, batch_size):
        # TODO: deprecate
        diag = np.eye(2 * batch_size)
        l1 = np.eye((2 * batch_size), 2 * batch_size, k=-batch_size)
        l2 = np.eye((2 * batch_size), 2 * batch_size, k=batch_size)
        mask = torch.from_numpy((diag + l1 + l2))
        mask = (1 - mask).type(torch.bool)
        if torch.cuda.is_available(): mask.to("cuda")
        return mask

    @staticmethod
    def _dot_simililarity(x, y):
        v = torch.tensordot(x.unsqueeze(1), y.T.unsqueeze(0), dims=2)
        # x shape: (N, 1, C)
        # y shape: (1, C, 2N)
        # v shape: (N, 2N)
        return v

    def _cosine_simililarity(self, x, y):
        # x shape: (N, 1, C)
        # y shape: (1, 2N, C)
        # v shape: (N, 2N)
        v = self._cosine_similarity(x.unsqueeze(1), y.unsqueeze(0))
        return v

    def forward(self, output, labels=None):
        """ Upon call

            Args:
                output: (torch.Tensor) Output from the model, shape: 2*bsz x d

            Returns:
                loss: (torch.Tensor) Contrastive Cross Entropy Loss

        """

        output = torch.nn.functional.normalize(output, dim=1)

        batch_size = output.shape[0] // 2
        similarity_matrix = self.similarity_function(output, output)

        # filter out the scores from the positive samples
        l_pos = torch.diag(similarity_matrix, batch_size)
        r_pos = torch.diag(similarity_matrix, -batch_size)
        positives = torch.cat([l_pos, r_pos]).view(2 * batch_size, 1)

        if self.correlated_mask is None or 2 * batch_size != self.correlated_mask.shape[0]:
            self.correlated_mask = self._torch_get_correlated_mask(batch_size)

        negatives = similarity_matrix[self.correlated_mask].view(2 * batch_size, -1)

        logits = torch.cat((positives, negatives), dim=1)
        logits /= self.temperature

        labels = torch.zeros(2 * batch_size).long()
        if torch.cuda.is_available(): labels.to("cuda")

        loss = self.cross_entropy(logits, labels.cuda())
        return loss / (2 * batch_size)
