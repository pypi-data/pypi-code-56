import re, sys, os
from rs4 import producers
from collections import Iterator
from aquests.athreads import trigger

def make_pushables (response, content):
    from .corequest import tasks
    from .wastuff.api import API
    from .corequest.pth import executors

    if not response.is_responsable ():
        # already called response.done () or diconnected channel
        return

    if content is None: # Possibly no return mistake
        raise AssertionError ("Content or part should not be None")

    if not content: # explicit empty not content
        trigger.wakeup (lambda p=response: (p.done(),))
        return

    if type (content) not in (list, tuple):
        content = (content,) # make iterable

    if isinstance (content [0], tasks.Revoke):
        return

    if isinstance (content [0], executors.Task):
        return

    if response ["content-type"] is None:
        response ["Content-Type"] = "text/html"

    will_be_push = []
    if len (response) == 0:
        content_length = 0
    else:
        content_length = None

    for part in content:
        # like Django response
        try: part = part.content
        except AttributeError: pass

        type_of_part = type (part)

        if isinstance (part, API):
            response.update ("Content-Type", part.get_content_type ())
            part = part.to_string ().encode ("utf8")
            will_be_push.append (part)

        elif type_of_part in (bytes, str):
            if len (part) == 0:
                continue
            if type_of_part is not bytes:
                try:
                    part = part.encode ("utf8")
                except AttributeError:
                    raise AssertionError ("%s is not supportable content type" % str (type (part)).replace ("<", "&lt;").replace (">", "&gt;"))
                type_of_part = bytes

            if type_of_part is bytes:
                if content_length is not None:
                    content_length += len (part)
                will_be_push.append (part)

        else:
            if hasattr (part, "read"):
                part = producers.closing_stream_producer (part)
            elif type (part) is list:
                part = producers.list_producer (part)
            elif isinstance(part, Iterator): # flask etc.
                part = producers.iter_producer (part)

            if hasattr (part, "more"):
                # producer
                content_length = None
                # automatic close    when channel suddenly closed
                hasattr (part, "close") and response.die_with (part)
                # streaming obj
                hasattr (part, "ready") and response.set_streaming ()
                will_be_push.append (part)

            else:
                raise AssertionError ("Unsupported response object")

    if content_length is not None:
        response ["Content-Length"] = content_length

    return will_be_push


def catch (format = 0, exc_info = None):
    if exc_info is None:
        exc_info = sys.exc_info()
    t, v, tb = exc_info
    tbinfo = []
    assert tb # Must have a traceback
    while tb:
        tbinfo.append((
            tb.tb_frame.f_code.co_filename,
            tb.tb_frame.f_code.co_name,
            str(tb.tb_lineno)
            ))
        tb = tb.tb_next

    del tb
    file, function, line = tbinfo [-1]

    # format 0 - text
    # format 1 - html
    # format 2 - list
    try:
        v = str (v)
    except:
        v = repr (v)

    if format == 1:
        if v.find ('\n') != -1:
            v = v.replace ("\r", "").replace ("\n", "<br>")
        buf = ["<div align='left'>"]
        buf.append ("<h3>%s</h3>" % t.__name__.replace (">", "&gt;").replace ("<", "&lt;"))
        buf.append ("<h4><div style='margin: 24px 0 6px;'>%s</div>" % v)
        buf.append ("<span style='font-weight: normal; color: #333;'>function <b>%s</b> file %s line <b>%s</b></span>" % (function == "?" and "__main__" or function, file, line))
        buf.append ("</h4>")

        buf.append ("<br><table width='100%' cellpadding='8' cellspacing='0'>")
        buf.append ("<tr bgcolor='#7A297B' style='color: #efefef; font-size: 12px;' align='left'><th>Path</th><th>File Name</th><th align='right'>Line#</th><th>Function</th></tr>")
        for i, x in enumerate (tbinfo):
            fi, fu, ln = x
            ba, fn = os.path.split (fi)
            bgcolor = i % 2 == 0 and 'fff' or 'efefef'
            if not fn.endswith ('.py'):
                bgcolor = i % 2 == 0 and 'FFFCCC' or 'FFFA99'
            buf += ["<tr bgcolor='#%s'><td style='word-break: break-all; color: #888;'>%s</td><td>%s</td><td class='n'><b>%s</b></td><td><span class='f'>%s</span></td></tr>" % (
                bgcolor,
                ba, fn, ln, fu
            )]
        buf.append ("</table></div>")
        return "\n".join (buf)

    buf = []
    buf.append ("%s %s" % (t, v))
    buf.append ("in file %s at line %s, %s" % (file, line, function == "?" and "__main__" or "function " + function))
    buf += ["%s %s %s" % x for x in tbinfo]
    if format == 0:
        return "\n".join (buf)
    return buf
