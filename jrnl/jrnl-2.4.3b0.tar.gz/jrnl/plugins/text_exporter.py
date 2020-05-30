#!/usr/bin/env python
# encoding: utf-8

import os

from ..util import ERROR_COLOR, RESET_COLOR, slugify


class TextExporter:
    """This Exporter can convert entries and journals into text files."""

    names = ["text", "txt"]
    extension = "txt"

    @classmethod
    def export_entry(cls, entry):
        """Returns a string representation of a single entry."""
        return str(entry)

    @classmethod
    def export_journal(cls, journal):
        """Returns a string representation of an entire journal."""
        return "\n".join(cls.export_entry(entry) for entry in journal)

    @classmethod
    def write_file(cls, journal, path):
        """Exports a journal into a single file."""
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(cls.export_journal(journal))
                return f"[Journal exported to {path}]"
        except IOError as e:
            return f"[{ERROR_COLOR}ERROR{RESET_COLOR}: {e.filename} {e.strerror}]"

    @classmethod
    def make_filename(cls, entry):
        return entry.date.strftime(
            "%Y-%m-%d_{}.{}".format(slugify(str(entry.title)), cls.extension)
        )

    @classmethod
    def write_files(cls, journal, path):
        """Exports a journal into individual files for each entry."""
        for entry in journal.entries:
            try:
                full_path = os.path.join(path, cls.make_filename(entry))
                with open(full_path, "w", encoding="utf-8") as f:
                    f.write(cls.export_entry(entry))
            except IOError as e:
                return "[{2}ERROR{3}: {0} {1}]".format(
                    e.filename, e.strerror, ERROR_COLOR, RESET_COLOR
                )
        return "[Journal exported to {}]".format(path)

    @classmethod
    def export(cls, journal, output=None):
        """Exports to individual files if output is an existing path, or into
        a single file if output is a file name, or returns the exporter's
        representation as string if output is None."""
        if output and os.path.isdir(output):  # multiple files
            return cls.write_files(journal, output)
        elif output:  # single file
            return cls.write_file(journal, output)
        else:
            return cls.export_journal(journal)
