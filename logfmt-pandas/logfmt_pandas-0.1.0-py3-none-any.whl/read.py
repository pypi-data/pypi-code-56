"""Read logfmt"""

from collections import abc
from io import StringIO
from itertools import islice
from pathlib import Path
from typing import Dict, Generator, Iterable, Optional
from os import PathLike

import logfmt
from pandas import DataFrame
from pandas.core.indexes.api import RangeIndex
from pandas.core.reshape.concat import concat


def read_logfmt(
    filepath_or_buffer, dtype=None, chunksize: Optional[int] = None,
):
    """
    Load a logfmt_ file.

    .. _logfmt: https://www.brandur.org/logfmt

    Returns
    -------
    `DataFrame` or `LogfmtReader`, if `chunksize` is specified.
    """

    logfmt_reader = LogfmtReader(filepath_or_buffer, dtype=dtype, chunksize=chunksize,)

    if chunksize:
        return logfmt_reader

    result = logfmt_reader.read()
    logfmt_reader.close()

    return result


class LogfmtReader(abc.Iterator):
    """
    LogfmtReader reads a logfmt file.
    """

    def __init__(self, filepath_or_buffer, dtype, chunksize: Optional[int],) -> None:
        self.chunksize = chunksize
        self.dtype = dtype
        self.nrows_seen = 0
        self.should_close = False

        if hasattr(filepath_or_buffer, "read"):
            self.data = filepath_or_buffer
        else:
            self.data = open(filepath_or_buffer, "r")
            self.should_close = True

    def read(self) -> DataFrame:
        """Read the rest of LogfmtReader as a single DataFrame"""
        return concat(self)

    def close(self) -> None:
        """
        Close a stream if we opened it earlier.
        """
        if self.should_close:
            self.data.close()

    @staticmethod
    def infer_types(lines: Iterable[Dict]) -> Generator[Dict, None, None]:
        """Infer types for parsed logfmt lines"""
        for line in lines:
            for key in line:
                try:
                    line[key] = int(line[key])
                except ValueError:
                    try:
                        line[key] = float(line[key])
                    except ValueError:
                        pass
            yield line

    def __next__(self):
        lines = list(islice(self.data, self.chunksize))
        if lines:
            logfmt_lines = self.infer_types(logfmt.parse(StringIO("\n".join(lines))))
            obj = DataFrame(logfmt_lines, dtype=self.dtype)

            obj.index = RangeIndex(self.nrows_seen, self.nrows_seen + len(obj))
            self.nrows_seen += len(obj)

            return obj

        self.close()
        raise StopIteration
