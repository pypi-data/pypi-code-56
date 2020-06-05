#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
OSD Neo2
========

On screen display for learning the keyboard layout Neo2

Copyright (c) 2009-2010 Martin Zuther (http://www.mzuther.de/)
Copyright (c) 2015-2020 Hartmut Goebel (http://crazy-compilers.com/)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

Thank you for using free software!

"""

# Here follows a plea in German to keep the comments in English so
# that you may understand them, dear visitor ...
#
# Meine Kommentare in den Quellcodes sind absichtlich auf Englisch
# gehalten, damit Leute, die im Internet nach Lösungen suchen, den
# Code nachvollziehen können.  Daher bitte ich darum, zusätzliche
# Kommentare ebenfalls auf Englisch zu schreiben.  Vielen Dank!


import ctypes
import ctypes.util
import collections

from .locale import _

"""
Far from complete wrapper for the "X Keyboard Extension" (well, to
be honest, it just wraps what I need using Python's "ctypes"
library <g>).
"""

# set this to true to get lots of debugging information (and
# considerably slow things down)
DEBUG_XKB = False

# "C defines" from file /usr/include/X11/extensions/XKB.h (Ubuntu 9.04):
# $XFree86: xc/include/extensions/XKB.h,v 1.5tsi Exp $
#
# XkbUseCoreKbd is used to specify the core keyboard without having to
# look up its X input extension identifier.

XkbUseCoreKbd            = 0x0100



# "C defines" from file /usr/include/X11/XKBlib.h (Ubuntu 9.04):
# $XFree86: xc/lib/X11/XKBlib.h,v 3.5 2003/04/17 02:06:31 dawes Exp $ #
#
# XkbOpenDisplay error codes

XkbOD_Success            = 0
XkbOD_BadLibraryVersion  = 1
XkbOD_ConnectionRefused  = 2
XkbOD_NonXkbServer       = 3
XkbOD_BadServerVersion   = 4

__XkbOD_error_names = {
    XkbOD_Success: 'XkbOD_Success',
    XkbOD_BadLibraryVersion: 'XkbOD_BadLibraryVersion',
    XkbOD_ConnectionRefused: 'XkbOD_ConnectionRefused',
    XkbOD_NonXkbServer: 'XkbOD_NonXkbServer',
    XkbOD_BadServerVersion: 'XkbOD_BadServerVersion',
}


# "C typedef" from file /usr/include/X11/extensions/XKBstr.h (Ubuntu 9.04):
# $Xorg: XKBstr.h,v 1.3 2000/08/18 04:05:45 coskrey Exp $
#
# Common data structures and access macros
#
# typedef struct _XkbStateRec {
#         unsigned char   group;
#         unsigned char   locked_group;
#         unsigned short  base_group;
#         unsigned short  latched_group;
#         unsigned char   mods;
#         unsigned char   base_mods;
#         unsigned char   latched_mods;
#         unsigned char   locked_mods;
#         unsigned char   compat_state;
#         unsigned char   grab_mods;
#         unsigned char   compat_grab_mods;
#         unsigned char   lookup_mods;
#         unsigned char   compat_lookup_mods;
#         unsigned short  ptr_buttons;
# } XkbStateRec,*XkbStatePtr;

class XkbStateRec(ctypes.Structure):
    _fields_ = [
                    ('group',              ctypes.c_ubyte),
                    ('locked_group',       ctypes.c_ubyte),
                    ('base_group',         ctypes.c_ushort),
                    ('latched_group',      ctypes.c_ushort),
                    ('mods',               ctypes.c_ubyte),
                    ('base_mods',          ctypes.c_ubyte),
                    ('latched_mods',       ctypes.c_ubyte),
                    ('locked_mods',        ctypes.c_ubyte),
                    ('compat_state',       ctypes.c_ubyte),
                    ('grab_mods',          ctypes.c_ubyte),
                    ('compat_grab_mods',   ctypes.c_ubyte),
                    ('lookup_mods',        ctypes.c_ubyte),
                    ('compat_lookup_mods', ctypes.c_ubyte),
                    ('ptr_buttons',        ctypes.c_ushort)
               ]

Time = ctypes.c_ulong    # from /usr/include/X11/X.h
KeyCode = ctypes.c_ubyte # from /usr/include/X11/X.h

# from /usr/include/X11/XKBlib.h
# https://www.x.org/releases/X11R7.7/doc/libX11/XKB/xkblib.html#Xkb_Event_Data_Structures
class XkbStateNotifyEvent(ctypes.Structure):
    _fields_ = [
        ('type',    ctypes.c_int),
        #('xkbtype', ctypes.c_int),
        ('serial', ctypes.c_ulong),       # number of last req processed by server
        ('send_event', ctypes.c_bool),    # is this from a SendEvent request?
        ('display', ctypes.c_void_p),     # Display the event was read from
        ('time', Time),                   # milliseconds
        ('xkb_type', ctypes.c_int),       # XkbStateNotify
        ('device', ctypes.c_int),         # device ID
        ('changed', ctypes.c_uint),       # mask of changed state components
        ('group', ctypes.c_int),          # keyboard group
        ('base_group', ctypes.c_int),     # base keyboard group
        ('latched_group', ctypes.c_int),  # latched keyboard group
        ('locked_group', ctypes.c_int),   # locked keyboard group
        ('mods', ctypes.c_uint),          # modifier state
        ('base_mods', ctypes.c_uint),     # base modifier state
        ('latched_mods', ctypes.c_uint),  # latched modifiers
        ('locked_mods', ctypes.c_uint),   # locked modifiers
        ('compat_state', ctypes.c_int),   # compatibility state
        ('grab_mods', ctypes.c_ubyte),        # mods used for grabs
        ('compat_grab_mods', ctypes.c_ubyte), # grab mods for non-XKB clients
        ('lookup_mods', ctypes.c_ubyte),      # mods sent to clients
        ('compat_lookup_mods', ctypes.c_ubyte), # mods sent to non-XKB clients
        ('ptr_buttons', ctypes.c_int),  # pointer button state
        ('keycode', KeyCode),           # keycode that caused the change
        ('event_type', ctypes.c_char),  # KeyPress or KeyRelease
        ('req_major', ctypes.c_char),   # Major opcode of request
        ('req_minor', ctypes.c_char),   # Minor opcode of request
]

class XEvent(ctypes.Union):
    _anonymous_ = ['state']
    _fields_ = [
        ('pad', ctypes.c_long * 24),
        ('state', XkbStateNotifyEvent),
        ]


# "C defines" from file /usr/include/X11/X.h (Ubuntu 9.04):
# $XFree86: xc/include/X.h,v 1.6 2003/07/09 15:27:28 tsi Exp $
#
# Key masks. Used as modifiers to GrabButton and GrabKey, results of
# QueryPointer, state in various key-, mouse-, and button-related
# events.

MASKS = collections.OrderedDict((
    ('ShiftMask',    1),
    ('LockMask',     2),
    ('ControlMask',  4),
    ('Mod1Mask',     8),
    ('Mod2Mask',    16), # NumLock
    ('Mod3Mask',    32),
    ('Mod4Mask',    64),
    ('Mod5Mask',   128),
))

# dynamically link to "X Keyboard Extension" library while at
# the same time checking which library to use
xkbd_library_location = ctypes.util.find_library('Xxf86misc')
if not xkbd_library_location:
    xkbd_library_location = ctypes.util.find_library('X11')
xkbd_library = ctypes.CDLL(xkbd_library_location)


# define "ctypes" prototype for the function
#
# Display *XkbOpenDisplay(display_name, event_rtrn, error_rtrn,
#                             major_in_out, minor_in_out, reason_rtrn)
#
#    char * display_name;
#    int * event_rtrn;
#    int * error_rtrn;
#    int * major_in_out;
#    int * minor_in_out;
#    int * reason_rtrn;

paramflags_xkbopendisplay = (
    (1, 'display_name'),
    (2, 'event_rtrn'),
    (2, 'error_rtrn'),
    (3, 'major_in_out'),
    (3, 'minor_in_out'),
    (2, 'reason_rtrn')
    )

prototype_xkbopendisplay = ctypes.CFUNCTYPE(
    ctypes.c_void_p,
        ctypes.c_char_p,
        ctypes.POINTER(ctypes.c_int),
        ctypes.POINTER(ctypes.c_int),
        ctypes.POINTER(ctypes.c_int),
        ctypes.POINTER(ctypes.c_int),
        ctypes.POINTER(ctypes.c_int)
        )

# set-up function (low-level)
__XkbOpenDisplay__ = prototype_xkbopendisplay(
    ('XkbOpenDisplay', xkbd_library),
        paramflags_xkbopendisplay
        )

# define error handler
def errcheck_xkbopendisplay(result, func, args):
    # print debugging information if requested
    if DEBUG_XKB:
        print()
        print('  [XkbOpenDisplay]')
        print('  Display:       %#010x' % result)
        for i, name in enumerate(('display_name: ',
                                  'event_rtrn:   ',
                                  'error_rtrn:   ',
                                  'major_in_out: ',
                                  'minor_in_out: ',
                                  'reason_rt:    ',
                              )):
            print(' ', name, args[i].value)

    # function didn't return display handle, so let's see why
    # not
    if result == 0:
        # values were taken from file /usr/include/X11/XKBlib.h (Ubuntu 9.04):
        # $XFree86: xc/lib/X11/XKBlib.h,v 3.5 2003/04/17 02:06:31 dawes Exp $ #
        error_id = args[5].value
        error_name = __XkbOD_error_names.get(error_id, 'undefined')
        error_message = (
            _('"XkbOpenDisplay" reported an error (%(error_name)s).') %
            {'error_name': _(error_name)} )
        raise OSError(error_message)

    # return display handle and all function arguments
    return (ctypes.c_uint(result), args)

# connect error handler to function
__XkbOpenDisplay__.errcheck = errcheck_xkbopendisplay



# define "ctypes" prototype for the function
#
# Bool XkbGetState(display, device_spec, state_return)
#
#     Display *             display;
#     unsigned int          device_spec;
#     XkbStatePtr           state_return;

paramflags_xkbgetstate = (
    (1, 'display'),
    (1, 'device_spec'),
    (3, 'state_return')
    )

prototype_xkbgetstate = ctypes.CFUNCTYPE(
    ctypes.c_int, # Python 2.5 doesn't yet know c_bool
        ctypes.c_void_p,
        ctypes.c_uint,
        ctypes.POINTER(XkbStateRec)
        )

# set-up function (low-level)
__XkbGetState__ = prototype_xkbgetstate(
    ('XkbGetState', xkbd_library),
        paramflags_xkbgetstate
        )

# define error handler
def errcheck_xkbgetstate(result, func, args):
    # print(debugging information if requested)
    if DEBUG_XKB:
        print()
        print('  [XkbGetState]')
        print('  Status:        %s' % result)
        print('  display:       %#010x' % args[0].value)
        print('  device_spec:   %d' % args[1].value)

        for g in ('group', 'locked_group', 'base_group',
                  'latched_group', 'mods', 'base_mods',
                  'latched_mods', 'locked_mods', 'compat_state',
                  'grab_mods', 'compat_grab_mods',
                  'lookup_mods', 'compat_lookup_mods',
                  'ptr_buttons'):
            print ('  state_return.%-20s' % (g+':'), getattr(args[2], g))
        print()
        print('  Mask          mods   base_mods  latched_mods'
              '  locked_mods   compat_state')
        print(' ', '-' * 72)
        for maskname, mask in MASKS.items():
            print('  %-12s  %-5s  %-10s %-14s %-13s %s' %
                  (maskname,
                   (args[2].mods         & mask) != 0,
                   (args[2].base_mods    & mask) != 0,
                   (args[2].latched_mods & mask) != 0,
                   (args[2].locked_mods  & mask) != 0,
                   (args[2].compat_state & mask) != 0))
    # return function return value and all function arguments
    return (result, args)

# connect error handler to function
__XkbGetState__.errcheck = errcheck_xkbgetstate


# define high-level version of "XkbOpenDisplay"
def XkbOpenDisplay(display_name, major_in_out, minor_in_out):
    # if we don't do type checking, nobody ever will
    assert isinstance(display_name, str) or display_name is None
    assert isinstance(major_in_out, int)
    assert isinstance(minor_in_out, int)

    # convert function arguments to "ctypes", ...
    __display_name__ = ctypes.c_char_p(display_name)
    __major_in_out__ = ctypes.c_int(major_in_out)
    __minor_in_out__ = ctypes.c_int(minor_in_out)

    # ... call low-level function ...
    ret = __XkbOpenDisplay__(__display_name__, __major_in_out__,
                                     __minor_in_out__)

    # Globally set the Xkb base event code, the X server assigns to
    # each X extension at runtime.
    global XkbBaseEventCode
    XkbBaseEventCode = ret[1][1].value

    # ... and return converted return value and function arguments
    return {'display_handle': ret[0].value,
                'server_major_version': ret[1][3].value,
                'server_minor_version': ret[1][4].value}


# define high-level version of "XkbGetState"
def XkbGetState(display_handle, device_spec):
    # if we don't do type checking, nobody ever will
    assert isinstance(display_handle, int)
    assert isinstance(device_spec, int)

    # convert function arguments to "ctypes", ...
    __display_handle__ = ctypes.c_void_p(display_handle)
    __device_spec__ = ctypes.c_uint(device_spec)
    __xkbstaterec__ = XkbStateRec()

    # ... call low-level function ...
    ret = __XkbGetState__(__display_handle__, __device_spec__,
                              __xkbstaterec__)

    # ... and return converted function argument
    xkbstaterec = ret[1][2]
    return xkbstaterec


# define "ctypes" prototype for the function
# https://www.x.org/archive/X11R7.5/doc/man/man3/XkbSelectEvents.3.html
#
# Bool XkbSelectEvents(display, device_spec, state_return)
#     Display *             display;
#     unsigned int          device_spec;
#     unsigned long int     bits_to_change
#     unsigned long int     values_for_bits

__XkbSelectEvents__ = xkbd_library.XkbSelectEvents
__XkbSelectEvents__.argtypes = [
    ctypes.c_void_p,
    ctypes.c_uint,
    ctypes.c_ulong,
    ctypes.c_ulong,
    ]
__XkbSelectEvents__.restype = ctypes.c_bool
XkbSelectEvents = __XkbSelectEvents__

XkbStateNotify = 2

XkbStateNotifyMask = 1<<2
XkbBellNotifyMask  = 1<<8
XkbAllEventsMask = 0xFFF


# define "ctypes" prototype for the function
# https://www.x.org/archive/X11R7.5/doc/man/man3/XNextEvent.3.html
#
# Bool XNextEvent(Display *display, XEvent *event_return)
#
#     Display *             display;
#     XEvent *              event_return

paramflags_xnextevent = (
    (1, 'display'),
    (3, 'xevent'),
    )

prototype_xnextevent = ctypes.CFUNCTYPE(
    ctypes.c_int,
        ctypes.c_void_p,
        ctypes.POINTER(XEvent)
        )

# set-up function (low-level)
__XNextEvent__ = prototype_xnextevent(
    ('XNextEvent', xkbd_library),
        paramflags_xnextevent
        )

# define error handler
def errcheck_xnextevent(result, func, args):
    # print(debugging information if requested)
    if DEBUG_XKB:
        xevent = args[1]
        print()
        print('  [XNextEvent]')
        print('  Status:        %s' % result)
        print('  display:       %#010x' % args[0].value)
        print('  type:          %d' % xevent.type)
        print('  xkbtype:       %d' % xevent.xkbtype)

        for g in ('group', 'locked_group', 'base_group',
                  'latched_group', 'mods', 'base_mods',
                  'latched_mods', 'locked_mods', 'compat_state',
                  'grab_mods', 'compat_grab_mods',
                  'lookup_mods', 'compat_lookup_mods',
                  'ptr_buttons'):
            print ('  state_return.%-20s' % (g+':'), getattr(xevent, g))
        print()
        print('  Mask          mods   base_mods  latched_mods'
              '  locked_mods   compat_state')
        print(' ', '-' * 72)
        for maskname, mask in MASKS.items():
            print('  %-12s  %-5s  %-10s %-14s %-13s %s' %
                  (maskname,
                   (xevent.mods         & mask) != 0,
                   (xevent.base_mods    & mask) != 0,
                   (xevent.latched_mods & mask) != 0,
                   (xevent.locked_mods  & mask) != 0,
                   (xevent.compat_state & mask) != 0))
    # return function return value and all function arguments
    return (result, args)

# connect error handler to function
__XNextEvent__.errcheck = errcheck_xnextevent

# define high-level version of "XNextEvent"
def XNextEvent(display_handle):
    # if we don't do type checking, nobody ever will
    assert isinstance(display_handle, int)

    # convert function arguments to "ctypes", ...
    __display_handle__ = ctypes.c_void_p(display_handle)
    __xevent__ = XEvent()
    # ... call low-level function ...
    ret = __XNextEvent__(__display_handle__, __xevent__)

    # ... and return converted function argument
    return ret[1][1]


def ConnectionNumber(display):
    """Hackish implementation of ConnectionNumber macro"""
    class _XPrivDisplay(ctypes.Structure):
        _fields_ = [
            ('ext_data',    ctypes.c_void_p),
            ('private1',    ctypes.c_void_p),
            ('fd', ctypes.c_int),
        ]
    return _XPrivDisplay.from_address(display).fd


XPending = xkbd_library.XPending
XPending.argtypes = [ctypes.c_void_p] # display


XSendEvent = xkbd_library.XSendEvent
XSendEvent.argtypes = [
    ctypes.c_void_p, # display
    ctypes.c_void_p, # windows
    ctypes.c_bool,   # propagate
    ctypes.c_long,   # event_mask
    ctypes.POINTER(XEvent)
]


XFlush = xkbd_library.XFlush
XFlush.argtypes = [ctypes.c_void_p] # display


XkbBellEvent = xkbd_library.XkbBellEvent
XkbBellEvent.argtypes = [
    ctypes.c_void_p, # display
    ctypes.c_void_p, # window or None
    ctypes.c_int,    # relative volume, from -100 to 100 inclusive
    ctypes.c_ulong,  # Atom name
]


# extract modifier status using bitmasks
def ExtractLocks(xkbstaterec):
    d = {'group': xkbstaterec.group}
    for name, maskname in (
        ('shift',   'ShiftMask'),
        ('lock',    'LockMask'),
        ('control', 'ControlMask'),
        ('mod1',    'Mod1Mask'),
        ('mod2',    'Mod2Mask'),
        ('mod3',    'Mod3Mask'),
        ('mod4',    'Mod4Mask'),
        ('mod5',    'Mod5Mask'),
        ):
        d[name] = (xkbstaterec.base_mods & MASKS.get(maskname)) != 0
    for name, maskname in (
        ('shift_lock',   'ShiftMask'),
        ('lock_lock',    'LockMask'),
        ('control_lock', 'ControlMask'),
        ('mod1_lock',    'Mod1Mask'),
        ('mod2_lock',    'Mod2Mask'),
        ('mod3_lock',    'Mod3Mask'),
        ('mod4_lock',    'Mod4Mask'),
        ('mod5_lock',    'Mod5Mask'),
        ):
        d[name] = (xkbstaterec.locked_mods & MASKS.get(maskname)) != 0
    return d


if __name__ == '__main__':
    # simple demonstration of this wrapper
    DEBUG_XKB = True

    # print debugging information
    print()
    print('  %s' % xkbd_library)

    # initialise wrapper for the X Keyboard Extension (v1.0) and
    # open connection to default X display
    display_name = None
    major_in_out = 1
    minor_in_out = 0

    try:
        ret = XkbOpenDisplay(display_name, major_in_out, minor_in_out)
    except OSError as error:
        print()
        print('  Error: %s' % error)
        print()
        exit(1)

    # ... get modifier state of core keyboard ...
    display_handle = ret['display_handle']
    device_spec = XkbUseCoreKbd
    xkbstaterec = XkbGetState(display_handle, device_spec)

    # ... and extract and the information we need
    mod_states = ExtractLocks(xkbstaterec)
    print()
    for mod in sorted(mod_states.keys()):
        print('  %-13s' % (mod + ':'), mod_states[mod])
    print()

    print('Now testing waiting for events')

    print('waiting for events … (press ctrl-c to interrupt)')
    XkbSelectEvents (display_handle, XkbUseCoreKbd,
                     XkbStateNotifyMask,
                     XkbAllEventsMask)
    try:
        while True:
            event = XNextEvent(display_handle)
            print('Got event', event.type, event.xkbtype)
    except KeyboardInterrupt:
        print("aborted by user request")
        pass
