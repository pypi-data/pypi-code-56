def dict_to_query_params(d: dict):
    NULL_VALUES = ['', None]
    if not d:
        return ''
    q_params = '?'
    for k, v in d.items():
        if v not in NULL_VALUES:
            q_params += f"{k}={v}&"
    return q_params.rstrip("&")
