def dict_to_query_params(d: dict):
    if not d:
        return ''
    q_params = '?'
    for k, v in d.items():
        q_params += f"{k}={v}&"
    return q_params.rstrip("&")