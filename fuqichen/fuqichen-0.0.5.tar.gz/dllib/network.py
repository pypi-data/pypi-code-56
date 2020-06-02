import torch


def count_parameters(model):
    return sum(p.numel() for p in model.parameters() if p.requires_grad)


def load_model(filename, model, device):
    try:
        checkpoint = torch.load(filename, map_location=device)
        model.load_state_dict(checkpoint['model'])
        meta = checkpoint.get('meta')
        print('{} Loaded'.format(filename))
    except Exception as e:
        print(e)
    return model, meta


def save_model(filename, model, meta):
    torch.save(
        {
            'model': model.state_dict(),
            'meta': meta
        },
        f=filename
    )
    print('{} Saved'.format(filename))
