# -*- coding: utf-8 -*-

"""Test that comments are ignored."""

import bibpy


def test_keep_comments():
    assert len(bibpy.read_file(
        'tests/data/all_bibpy_entry_types.bib',
        ignore_comments=False
    ).comments) == 1


def test_ignore_comments():
    assert len(bibpy.read_file(
        'tests/data/all_bibpy_entry_types.bib',
        ignore_comments=True
    ).comments) == 0
