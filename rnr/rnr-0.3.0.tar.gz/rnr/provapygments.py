#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os

from pprint import pprint

import pygments

import pygments
import pygments.lexers
import pygments.util

import urwid

from pygments.token import Token

from .debug_print import (debug_print, debug_pprint)


PALETTE = [
	('Text', 'yellow', 'dark blue'),
	('Namespace', 'light green', 'dark blue'),
	('Keyword', 'white', 'dark blue'),
	('Class', 'light red', 'dark blue'),
	('Literal', 'light cyan', 'dark blue'),
	('Comment', 'light gray', 'dark blue'),
	('Lineno', 'light cyan', 'dark blue'),
]

StyleFromToken = {
	Token.Keyword.Namespace: 'Namespace',
	Token.Keyword: 'Keyword',
	Token.Name.Class: 'Class',
	Token.Name.Function: 'Class',
	Token.Name.Tag: 'Keyword',
	Token.Name.Attribute: 'Class',
	Token.Literal: 'Literal',
	Token.Operator: 'Keyword',
	Token.Comment.Preproc: 'Namespace',
	Token.Comment: 'Comment',
}

filename = 'panel.py'
with open(filename) as fh:
	code = fh.read()

	lines = []

	try:
		lexer = pygments.lexers.get_lexer_for_filename(filename, stripnl=False, tabsize=4)
	except pygments.util.ClassNotFound:
		pass

	print(repr(lexer))

	line = []
	result = pygments.lex(code, lexer)
	for tokentype, value in result:
		#pprint((tokentype, value))
		for k, v in StyleFromToken.items():
			if tokentype in k:
				style = v
				break
		else:
			style = 'Text'

		for l in value.splitlines(keepends=True):
			line.append((style, l.rstrip('\n')))
			if '\n' in l:
				lines.append(line)
				line = []

	digits = len(str(len(lines)))
	lst = [urwid.Columns([(digits, urwid.Text(('Lineno', f'{i+1}'), align='right')), urwid.Text(x, wrap='clip')], dividechars=1) for i, x in enumerate(lines)]
	w = urwid.SimpleListWalker(lst)
	w = urwid.ListBox(w)
	w = urwid.AttrMap(w, 'Text')

	loop = urwid.MainLoop(w, PALETTE)
	loop.run()

