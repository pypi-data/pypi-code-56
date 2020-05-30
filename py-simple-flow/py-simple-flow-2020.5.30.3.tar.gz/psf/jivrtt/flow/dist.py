import multiprocessing
import time


def apply(target_func, tasks, args=None, kwargs=None, num_of_buckets=1, bucket_size=1, wait_for_completion=True):
    run_local = num_of_buckets == 1
    args = args or list()
    kwargs = kwargs or dict()
    if run_local:
        target_func(tasks, *args, **kwargs)
    else:
        _run_multi_process(
            target_func,
            tasks,
            args=args,
            kwargs=kwargs,
            num_of_buckets=num_of_buckets,
            bucket_size=bucket_size,
            wait_for_completion=wait_for_completion,
        )


def _run_multi_process(
        target_func,
        tasks,
        args=None,
        kwargs=None,
        num_of_buckets=5,
        bucket_size=1,
        wait_for_completion=True
):
    buckets = map(lambda idx: tasks[idx:idx + bucket_size], range(0, len(tasks), bucket_size))
    processes = []
    for bucket_idx, bucket in enumerate(buckets, 1):
        _limit_processes(bucket_idx, processes, num_of_buckets)
        args_to_pass = tuple([bucket] + list(args))
        process = _start_processes(target_func, args=args_to_pass, kwargs=kwargs)
        processes.append(process)
    list(map(lambda prc: prc.join() if wait_for_completion else None, processes))
    total_complete = sum(map(lambda prc: 1 if prc.exitcode is not None else 0, processes))
    print(f'Total buckets processed: {len(processes)}. Total completed {total_complete}')


def _start_processes(
        target_func,
        args=None,
        kwargs=None,
):
    process = multiprocessing.Process(target=target_func, args=args, kwargs=kwargs, daemon=True)
    process.start()
    return process


def _limit_processes(bucket_idx, processes, num_of_buckets):
    total_complete = sum(map(lambda prc: 1 if prc.exitcode is not None else 0, processes))
    while (bucket_idx - total_complete) >= num_of_buckets:
        print(f'Waiting for processes to complete. Max processes {num_of_buckets} running already..')
        total_complete = sum(map(lambda prc: 1 if prc.exitcode is not None else 0, processes))
        time.sleep(0.25)
    print(f'Limit check complete. Total processes started: {len(processes)}, total complete {total_complete}..')
