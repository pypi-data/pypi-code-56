#!/usr/bin/env python
#coding=utf8
"""
Gnuplot for python
"""

import sys, os, string, types
import collections
import subprocess
try:
    # Python 2.
    from StringIO import StringIO
    # Python 3.
except ImportError:
    from io import StringIO
#import numpy as np  
#import pandas as pd

def make_plot(*args, **kwargs):
    subplot = {'subtype': 'plot',
            'cmd': [] }
    subplot["attribute"] = collections.OrderedDict()

    subplot["attribute"] = collections.OrderedDict()

    for v in args:
        subplot["cmd"].append(v)
    for k,v in kwargs.items():
        subplot["attribute"][k] = v
    return subplot

def make_splot(*args, **kwargs):
    subplot = {'subtype': 'splot',
            'cmd': [] }
    subplot["attribute"] = collections.OrderedDict()

    for v in args:
        subplot["cmd"].append(v)
    for k,v in kwargs.items():
        subplot["attribute"][k] = v
    return subplot

def multiplot(*args, **kwargs):
    '''
    @args: the subplot object list;
    @kwargs: the setting options that need to be set before call plot;
    '''
    g = Gnuplot()

    for k,v in kwargs.items():
        g.cmd('set %s %s' %(k, v))
    if 'multiplot' not in kwargs.keys():
        g.cmd('set multiplot')

    #print(args)
    for subplot in args:
        g.set(**subplot["attribute"])
        cmd = subplot["cmd"]
        c = subplot["subtype"]
        for cmd in subplot["cmd"]:
            c += ' %s,' %(cmd)
        #print("log multiplot(): ", c.rstrip(','))
        g.cmd(c.rstrip(','))
        # multiplot automatically unset the following setting:
        g.unset('for [i=1:200] label i')
        #g.unset('for [i=1:200] label i',
        #        'title',
        #        'xtics', 'x2tics', 'ytics', 'y2tics', 'ztics', 'cbtics',
        #        'xlabel', 'x2label', 'ylabel', 'y2label', 'zlabel', 'cblabel',
        #        'xrange', 'x2range', 'yrange', 'y2range', 'zrange', 'cbrange',
        #        'rrange', 'trange', 'urange', 'vrange')
    g.reset()

def plot(*args, **kwargs):
    '''
    *items: The list of plot command;
    **kwargs: The options that would be set before the plot command.
    '''
    __gnuplot("plot", *args, **kwargs)

def splot(*args, **kwargs):
    __gnuplot("splot", *args, **kwargs)

def __gnuplot(plot_cmd, *args, **kwargs):
    g = Gnuplot()
    g.set(**kwargs)
    c = plot_cmd
    for cmd in args:
        c += ' %s,' %(cmd)
    #print(c.rstrip(','))
    g.cmd(c.rstrip(','))
    g.reset()

class Gnuplot(object):
    """Unsophisticated interface to a running gnuplot program.

    See gp_unix.py for usage information.

    """

    def __init__(self, *args, **kwargs):
        '''
        attributes and kwargs are non-ordered, if there is order requirement,
        please call set many times in order after init.
        '''
        self.gnuplot = subprocess.Popen(['gnuplot','-p'], shell=True, stdin=subprocess.PIPE)
        # forward write and flush methods:
        self.write = self.gnuplot.stdin.write
        self.flush = self.gnuplot.stdin.flush

        for v in args:
            self.cmd('set %s' %(v))
        for k,v in kwargs.items():
            #self[k] = v
            self.cmd('set %s %s' %(k, v))

    def __del__(self):
        #print("%s:%d" %(os.path.basename(__file__), sys._getframe().f_lineno))
        self.close()

    def cmd(self, *args):
        '''
        *args: all the line that need to pass to gnuplot. It could be a list of
        lines, or a paragraph; Lines starting with "#" would be omitted. Every
        line should be a clause that could be executed in gnuplot.
        '''
        commands = []
        for cmd in args:
            #print StringIO(cmd.strip()).readlines()
            cmd = filter(lambda x: (x.strip()) and (x.strip()[0] != '#'),
                    StringIO(cmd.strip()).readlines())
            # remove the leading or trailing \r\n
            commands += map(lambda x: x.strip(), cmd)

        for c in commands:
            #print("\033[1;34m[py-gnuplot]\033[0m%s" %(c))
            self.__call__('%s' %(c))

    def close(self):
        if self.gnuplot is not None:
            self.gnuplot.stdin.write(bytes('quit\n', encoding = "utf8")) #close the gnuplot window
            self.gnuplot = None

    def abort(self):
        if self.gnuplot is not None:
            self.gnuplot.kill()
            self.gnuplot = None

    def cd(self, path):
        self.cmd('cd %s' %(path))

    def call(self, filename, *items):
        params = ""
        for item in items:
            params += " " + item
        self.cmd('call "%s" %s' %(filename, params))

    def clear(self):
        self.cmd('clear')

    def do(self, iteration, *commands):
        self.cmd('do %s {' %(iteration))
        for cmd in commands:
            self.cmd('%s' %(cmd))
        self.cmd('}')

    def set(self, *args, **kwargs):
        '''
        *args: options without value
        *kwargs: options with value. The set and unset commands may optionally
                 contain an iteration clause, so the arg could be list.
        '''
        for v in args:
            #print('set %s' %(v))
            self.cmd('set %s' %(v))
        for k,v in kwargs.items():
            if isinstance(v, list):
                for i in v:
                    #print('set %s %s' %(k, i))
                    self.cmd('set %s %s' %(k, i))
            else:
                #print('set %s %s' %(k, v))
                if (v == None):
                    self.cmd('unset %s' %(k))
                else:
                    self.cmd('set %s %s' %(k, v))

    def unset(self, *items):
        '''
        *args: options that need to be unset
        '''
        for item in items:
            self.cmd('unset %s\n' %(item))

    def reset(self):
        self.cmd('reset')

    def plot(self, *items, **kwargs):
        '''
        *items: The list of plot command;
        **kwargs: The options that would be set before the plot command.
        '''
        self.set(**kwargs)
        c = 'plot'
        for item in items:
            c = c + " " + item + ","
        cmd = c.rstrip(',')
        self.cmd(cmd + '\n')

    # print function couldn't be compiled.
    #def print(self, *items):
    #    c = 'print'
    #    for item in items:
    #        c = c + " " + item + ","
    #    cmd = c.rstrip(',')
    #    self.cmd(cmd + '\n')

    def splot(self, *items, **kwargs):
        self.set(**kwargs)
        c = 'splot'
        for item in items:
            c = c + " " + item + ","
        cmd = c.rstrip(',')
        self.cmd(cmd + '\n')


    def evaluate(self, cmd):
        self.cmd('evaluate %s' %(cmd))

    def exit(self):
        self.cmd('exit')

    def fit(self, cmd):
        #TODO: to be done.
        self.cmd('fit %s' %(cmd))

    def help(self, cmd):
        self.cmd('help %s\r\n' %(cmd))

    def history(self, cmd):
        self.cmd('history %s' %(cmd))

    def load(self, filename):
        self.cmd('load %s' %(cmd))

    def pause(self, param):
        self.cmd('pause %s\n' %(param))

    def __getitem__(self, name): return self.__dict__.get(name.lower(), None)

    def __setitem__(self, name, value):
        #print name,value
        self.cmd('set %s %s\n' %(name, value))

    def __call__(self, s):
        """Send a command string to gnuplot, followed by newline."""
        #print(s)
        cmd = s + '\n'
        self.write(cmd.encode('utf-8'))
        self.flush()

if __name__ == '__main__':
    g = Gnuplot()
    #ts = pd.Series(np.random.randn(10))
