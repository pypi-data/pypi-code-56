"""
Coalesce multiple identical call into one, preventing thundering-herd/stampede to database/other backends

python port of https://github.com/golang/groupcache/blob/master/singleflight/singleflight.go

consists of 3 implementation

    basic

    gevent

    asynchronous
  
"""

__version__ = "0.1.0"
