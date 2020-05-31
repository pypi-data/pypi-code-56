import os
import time
import tempfile
import memory_profiler
import humanize
import pandas as pd
from . import extractors as ext


# Note on memory_profiler:
#   ?memory_profiler.memory_usage
#   proc : The tuple contains three values (f, args, kw) and specifies to run the function f(*args, **kw).
#   memory usage, in MiB
def save_profiler(
        self,
        writer,
        writer_args=None,
        reader='infer',
        reader_args=None,
        path=None,
        keep=False,
        repeats=5,
        repeats_summary_function='mean',
        test_read_back=True,
        sleep_time=1,
        **kwargs
):
    """
    Evaluates pandas performance when saving and reloading dataframes.

    Parameters
    ----------
    self : dataframe
        The dataframe to be saved.
    writer : str
        The writing method, for instance 'to_pickle' or 'to_parquet'.
    writer_args: dict or None
        kwargs to be pasted to the writing method.
    reader : str or None
        The reading function used to reload the saved data, for instance 'read_pickle'.
        When set to 'infer' it is inferred from the writer name.
        If None, the reload of the dataframe is not done.
    reader_args : dict or None
        kwargs to be pasted to the reader function.
    path : str or None
       Path to the file to be saved. If None the function automatically uses a temporary file.
    keep : bool
       If True and a path is given then the saved file is not deleted after the evaluation.
    repeats : int
       Number of times the file is saved. Reported statistics will be an average of all repeats.
    repeats_summary_function : str
       Name of the function used to summarize the output statistics.
       Can be any pandas Series method. Default is set to 'mean'.
    test_read_back : bool
        If True and the reader is not None then the functions tests that the
        reloaded dataframe is the same as the saved one.
    sleep_time : float
        Sleep time between repeats of the saving process or between saving and reading back.
        Leaving this lag time may give more accurate measures of the memory usage.
    **kwargs : keywords
        Options to pass to the writer method.

    Returns
    -------
    A pandas series with the following items:

        format : the format of the saved file.
        writer : method used to save or write the dataframe.
        reader : pandas function used to reload the dataframe.
        writer_args : arguments passed to the writing method.
        reader_args : arguments passed to the reading function.

        writer_time : writing time in seconds.
        reader_time : reading or reloading time in seconds.

        writer_memory : maximum memory pick used to write the dataframe (in bytes).
        reader_memory : maximum memory pick used to reload the dataframe (in bytes).
        df_memory : total memory used by the dataframe as reported by
                    pandas.DataFrame.memory_usage (in bytes).
        file_size : file size (in bytes).

        writer_memory_h: humanized version of the writer_memory.
        reader_memory_h: humanized version of the reader_memory.
        df_memory_h: humanized version of the df_memory.
        file_size_h: humanized version of the file_size.

        repeats: number of times the writing process was repeated.
        reads_the_same: boolean flag indicating if the reloaded dataframe
                        is exactly the same as the original one or not.
                        Can be None if the reader is not used.
    """

    if reader == 'infer':
        reader = writer.replace('to_', 'read_')

    if writer_args is None:
        writer_args = {k: v for k, v in kwargs.items() if k in ext.extract_writer_arguments(writer)}

    if (reader_args is None) & (reader is not None):
        reader_args = {k: v for k, v in kwargs.items() if k in ext.extract_reader_arguments(reader)}

    # set path arguments
    if path is None:
        tmp = tempfile.NamedTemporaryFile()
        file = tmp.name
        if keep is None:
            keep = False
    else:
        file = path
        if keep is None:
            keep = True

    writer_path_argument = ext.extract_writer_path_argument(writer)
    writer_args[writer_path_argument] = file

    if reader is not None:
        reader_path_argument = ext.extract_reader_path_argument(reader)
        reader_args[reader_path_argument] = file

    # write
    writer_times = []
    write_memories = []
    print(' ', writer, end='')
    for _ in range(repeats):
        print('.', end='', flush=True)
        pd_to = getattr(self, writer)
        t0 = time.perf_counter()
        memory = memory_profiler.memory_usage((pd_to, (), writer_args), max_iterations=1, max_usage=True)
        t1 = time.perf_counter()
        writer_times.append(t1 - t0)
        write_memories.append(memory * (1024 ** 2))  # memory usage from MiB to bytes
        time.sleep(sleep_time)
    writer_time = getattr(pd.Series(writer_times), repeats_summary_function)()
    writer_memory = getattr(pd.Series(write_memories), repeats_summary_function)()

    print()

    # read
    if reader:
        reader_times = []
        read_memories = []
        print(reader, end='')
        for _ in range(repeats):
            print('.', end='', flush=True)
            pd_read = getattr(pd, reader)
            t0 = time.perf_counter()
            memory, data = memory_profiler.memory_usage((pd_read, (), reader_args), max_iterations=1, max_usage=True, retval=True)
            t1 = time.perf_counter()
            reader_times.append(t1 - t0)
            read_memories.append(memory * (1024 ** 2))
            time.sleep(sleep_time)
        reader_time = getattr(pd.Series(reader_times), repeats_summary_function)()
        reader_memory = getattr(pd.Series(read_memories), repeats_summary_function)()

        if test_read_back:
            try:
                pd.testing.assert_frame_equal(self, data)
                reads_back_ok = True
            except Exception:
                reads_back_ok = False
        else:
            reads_back_ok = None
    else:
        reader_time = None
        reader_memory = 0  # change to None
        reads_back_ok = None

    print()

    # file size
    try:      # the try here is a patch for to_sql
        file_size = os.path.getsize(file)
    except Exception:
        print('File not found')
        file_size = 0  # change to None

    # data frame memory usage
    df_memory = self.memory_usage().sum()

    # clean temp file
    if not keep:
        if path:
            os.remove(path)
        else:
            tmp.close()

    # output
    res = {
        'format': writer.replace('to_', ''),
        'writer': writer,
        'reader': reader,
        'writer_args': writer_args,
        'reader_args': reader_args,
        'writer_time': writer_time,
        'reader_time': reader_time,
        'writer_memory': writer_memory,
        'reader_memory': reader_memory,
        'df_memory': df_memory,
        'file_size': file_size,

        'writer_memory_h': humanize.naturalsize(writer_memory),
        'reader_memory_h': humanize.naturalsize(reader_memory),
        'df_memory_h': humanize.naturalsize(df_memory),
        'file_size_h': humanize.naturalsize(file_size),

        'repeats': repeats,
        'reads_the_same': reads_back_ok,
    }

    if keep:
        res['path'] = file

    res = pd.Series(res)

    return res


pd.core.frame.DataFrame.save_profiler = save_profiler
