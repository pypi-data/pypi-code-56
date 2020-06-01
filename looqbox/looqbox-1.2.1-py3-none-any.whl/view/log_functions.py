from looqbox.global_calling import GlobalCalling


__all__ = ["log_query"]


def log_query(*args):
    query_list = GlobalCalling.looq.query_list
    queries = [*args]

    for i in range(1, len(queries)):
        query_list = query_list.append(queries[i])

    print(query_list)