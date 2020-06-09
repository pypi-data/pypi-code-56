# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import torch
import torch.nn as nn


def wsify(module: nn.Module) -> None:
    with torch.no_grad():
        update_conv(module)
        replace_bn(module)


def update_conv(module: nn.Module) -> None:
    for child in module.children():
        if len(list(child.children())) > 0:
            update_conv(child)

        if isinstance(child, nn.Conv2d):
            p = child.weight
            p_lm = p - p.mean(dim=1, keepdim=True).mean(dim=2, keepdim=True).mean(dim=3, keepdim=True)
            ws_std = p_lm.view(p_lm.size(0), -1).std(dim=1).view(-1, 1, 1, 1) + 1e-5
            child.weight.copy_((p - p_lm) / ws_std)


def replace_bn(module: nn.Module, num_groups: int = 4) -> None:
    for name, child in module.named_children():
        if len(list(child.children())) > 0:
            replace_bn(child)

        if isinstance(child, nn.BatchNorm2d):
            module._modules[name] = nn.GroupNorm(num_groups, child.num_features, affine=False)
