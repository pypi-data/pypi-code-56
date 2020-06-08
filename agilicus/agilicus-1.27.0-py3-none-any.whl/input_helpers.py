from . import context


def get_org_from_input_or_ctx(ctx, org_id=None, **kwargs):
    if org_id is None:
        token = context.get_token(ctx)
        org_id = context.get_org_id(ctx, token)

    # Treat an empty-string org id like None so that we can query all if necessary
    if org_id == "":
        org_id = None

    return org_id
