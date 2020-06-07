import torch
import torch.nn.functional as F
from torch import nn
from functools import partial

# constants

DEFAULT_PSI = lambda x: F.elu(x) + 1

# helper functions

def default(val, d):
    return val if val is not None else d

def safe_div(n, d, eps = 1e-6):
    return n.div_(d + eps)

# self attention layer

def linear_attn(q, k, v, one_kv_head = False):
    q = q.softmax(dim=-1)
    k = k.softmax(dim=-2)

    context_einsum_eq = 'bhnd,bhne->bhde' if not one_kv_head else 'bnd,bne->bde'
    context = torch.einsum(context_einsum_eq, k, v)

    attn_einsum_eq = 'bhnd,bhde->bhne' if not one_kv_head else 'bhnd,bde->bhne'
    attn = torch.einsum(attn_einsum_eq, q, context)

    return attn.reshape(*q.shape)

def causal_linear_attn(q, k, v, psi = DEFAULT_PSI, one_kv_head = False, bucket_size = None):
    b, h, n, e, dtype = *q.shape, q.dtype
    bucket_size = default(bucket_size, 64)

    q = q.softmax(dim=-1)
    k = psi(k)

    bucket_fn = lambda x: x.reshape(*x.shape[:-2], -1, bucket_size, e)
    b_q, b_k, b_v = map(bucket_fn, (q, k, v))

    b_k_sum = b_k.sum(dim=-2)
    b_k_cumsum = b_k_sum.cumsum(dim=-2).type(dtype)

    context_einsum_eq = 'bhund,bhune->bhude' if not one_kv_head else 'bund,bune->bude'
    context = torch.einsum(context_einsum_eq, b_k, b_v)
    context_cumsum = context.cumsum(dim=-3).type(dtype)

    context = safe_div(context_cumsum, b_k_cumsum.unsqueeze(-1))

    if bucket_size != 1:
        context = F.pad(context, (0, 0, 0, 0, 1, 0), value=0.)
        seq_dim = 1 if one_kv_head else 2
        context, _ = split_at_index(seq_dim, -1, context)

    attn_einsum_eq = 'bhund,bhude->bhune' if not one_kv_head else 'bhund,bude->bhune'
    attn = torch.einsum(attn_einsum_eq, b_q, context)
    return attn.reshape(*q.shape)

class LinearSelfAttention(nn.Module):
    def __init__(self, dim, heads, causal, one_kv_head = False, psi_fn = DEFAULT_PSI, blindspot_size = 1):
        super().__init__()
        assert (dim % heads) == 0, 'embedding dimension must be divisible by number of heads'
        d_heads = dim // heads
        self.heads = heads
        self.psi_fn = psi_fn

        self.global_attn_fn = linear_attn if not causal else partial(causal_linear_attn, psi=psi_fn, bucket_size = blindspot_size)

        self.to_q = nn.Linear(dim, dim, bias = False)

        kv_heads = 1 if one_kv_head else heads
        self.one_kv_head = one_kv_head
        self.kv_heads = kv_heads
        self.to_k = nn.Linear(dim, d_heads * kv_heads, bias = False)
        self.to_v = nn.Linear(dim, d_heads * kv_heads, bias = False)

        self.to_out = nn.Linear(dim, dim)


    def forward(self, x, input_mask = None, **kwargs):
        q, k, v = (self.to_q(x), self.to_k(x), self.to_v(x))

        b, t, e, h = *q.shape, self.heads
        merge_heads = lambda x: x.reshape(b, t, h, -1).transpose(1, 2)

        q = merge_heads(q)

        if not self.one_kv_head:
            k, v = map(merge_heads, (k, v))

        attn = self.global_attn_fn(q, k, v, one_kv_head = self.one_kv_head)
        attn = attn.transpose(1, 2).reshape(b, t, -1)
        return self.to_out(attn)

# image attention

class LinearImageAttention(nn.Module):
    def __init__(self, chan, key_dim = 64, value_dim = 64, heads = 8):
        super().__init__()

        self.chan = chan
        self.key_dim = key_dim
        self.value_dim = value_dim
        self.heads = heads
        
        self.to_q = nn.Conv2d(chan, key_dim * heads, 1)
        self.to_k = nn.Conv2d(chan, key_dim, 1)
        self.to_v = nn.Conv2d(chan, value_dim, 1)
        self.to_out = nn.Conv2d(value_dim * heads, chan, 1)

    def forward(self, x):
        b, _, h, w = x.shape

        q, k, v = (self.to_q(x), self.to_k(x), self.to_v(x))

        q = q.reshape(b, self.heads, -1, h * w)
        k = k.reshape(b, -1, h * w)
        v = v.reshape(b, -1, h * w)

        k = k.softmax(dim=2)
        q = q.softmax(dim=2)

        context = torch.einsum('bdn,ben->bde', k, v)
        out = torch.einsum('bhdn,bde->bhen', q, context)
        out = out.reshape(b, -1, h, w)
        out = self.to_out(out)
        return out