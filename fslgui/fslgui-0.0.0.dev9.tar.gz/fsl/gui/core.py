"""
core functions for setting up and controlling GUIs

"""
import os
import sys
import json

import wx
import yaml
import fsleyes_props as props

from fsl.utils import idle
import fsl.gui.exceptions as fslerrs
import fsl.gui.widgets as fslwidgets

allowedContainerWidgets = (
    'column', 'row', 'group',
    'page', 'notebook'
    )

allowedWidgets = (
    *allowedContainerWidgets, 
    'filepath', 'checkbox', 'choice',
    'number', 'button', 'FsleyesImage',
    'point'
)

allowedConfigKeys = (
    'appName', 'windowSize', 'width',
    'height', 'layout',
    )

allowedKeys = (
    *allowedConfigKeys,
    *allowedWidgets,
    )


def runCommand(propObj, button):
    """
    if a propObj has a run method, then this funnction will call it
    and run it on the idle loop. 
    """
    if hasattr(propObj, "run"):
        idle.run(propObj.run, onFinish=updateStatus)
        updateStatus("BUSY")
    else:
        print(propObj, " has no attribute: run")

def updateStatus(msg="IDLE"):
    """
    if a frame has a statusbar then set its text with msg.
    Useful for indicating "busy" or "idle" for jobs runnining on another thread
    """
    tlw = wx.GetTopLevelWindows()[0]
    if hasattr(tlw, "statusbar"):
        tlw.statusbar.SetStatusText(msg)


def isGroupKey(key):
    """
    returns True is key == "group"

    returns False otherwise
    """
    if key == "group":
        return True
    else:
        return False

def isPageKey(key):
    """
    returns True is key == "group"

    returns False otherwise
    """
    if key == "page":
        return True
    else:
        return False

def isContainerKey(key):
    """
    returns True if this key is associated with a container widget
    from allowedContainerWidgets.

    returns False otherwise

    a container widget is not really intereactive for the user.
    it holds other widgets as children
    """
    if key in allowedContainerWidgets:
        return True
    else:
        return False

def loadSpec(specFile):
    """
    return the loaded yaml data as a dict
    """
    with open(specFile) as sf:
        spec = yaml.load(sf, Loader=yaml.FullLoader)
    return spec

def checkSpec(buildSpec):
    """
    make sure the build spec contains only expected fields
    """
    def dictCheck(d):
        if type(d) is list:
            for entry in d:
                print(entry)
                for k, v in entry.items():
                    k, _ = parseWidgetKey(k)
                    if k not in allowedKeys:
                        raise fslerrs.NotAValidKey("{} is not an allowed buildSpec key".format(k))
                    if type(v) is dict:
                        dictCheck(v)
    dictCheck(buildSpec)


def layoutFrom(widget):
    """
    redo layout of all widgets up the parent tree from this widget.
    Stop when we get to a frame. This was taken from a wx wiki post
    """
    while widget.GetParent():
        widget.Layout()
        widget = widget.GetParent()
        widget.Layout()
        if widget.IsTopLevel():
            break

def parseWidgetKey(key):
    """
    returns string tuple (key, tag)

    the string "key" must not contain more than one underscore
    """
    parts = key.split(sep="_")
    t = ""
    if len(parts) == 1:
        n = parts[0]
    elif len(parts) == 2:
        n = parts[0]
        t = parts[-1]
    elif len(parts) > 2:
        raise Exception("keys must be in the forms 'key' or 'key_name'")
    else:
        n = ""
    return n, t

def isGroup(widget):
    if isinstance(widget.GetSizer(), wx.StaticBoxSizer):
        return True
    else:
        return False

def isNotebook(widget):
    if isinstance(widget, wx.Notebook):
        return True
    else:
        return False

def isPage(widget):
    if isinstance(widget.GetParent(), wx.Notebook):
        return True
    else:
        return False

def addWidgetToGroup(parent, widget):
    w = widget(parent.GetSizer().GetStaticBox())
    return w

def addPageToNotebook(parent, widget, name):
    parent.AddPage(widget, name)
    return widget


def widgetFromKey(key):
    """
    returns the appropriate widget creation function,
    but does not return the actual widget instance.
    That comes later.
    """
    widget = getattr(fslwidgets, key)
    return widget

def popStyle(v):
    if type(v) is dict and "style" in v.keys():
        style = v.pop("style")
        flag = style["flag"]
        att = getattr(wx, flag, 0)
        return att
    else:
        return 0

def makeWidget(parent, propObj, key, tag, value):
    """
    returns the appropriate widget from a key string

    key:    str parsed from the form "key_tag" or "key"
    tag:    str parsed from the form "key_tag" 
    value:  the dict value for this key. Only value==dict is used here

    """
    if key in allowedWidgets:
        wid = widgetFromKey(key)
        # print('making widget: ', key)
        if isinstance(value, dict):
            w = wid(parent, propObj, **value)
        else:
            if isGroupKey(key):
                w = wid(parent, tag)
            else:
                if isGroup(parent):
                    w = addWidgetToGroup(parent, wid)
                elif isNotebook(parent):
                    w = wid(parent)
                    w = addPageToNotebook(parent, w, tag)
                else:
                    w = wid(parent)
    return w

def addToParent(parent, widget, style=0, proportion=0, defflags=wx.ALL | wx.EXPAND, border=5):
    if style == wx.CENTER:
        parent.GetSizer().AddStretchSpacer(prop=1)
        parent.GetSizer().Add(widget, proportion=0, flag=defflags | style, border=border)
        parent.GetSizer().AddStretchSpacer(prop=1)
    else:
        parent.GetSizer().Add(widget, proportion=0, flag=defflags | style, border=border)

def layout(parent, buildSpec, propObj):
    """
    layout all allowed widgets in a buildSpec
    """
    for entry in buildSpec:
        for k, v in entry.items():
            k, t = parseWidgetKey(k)
            style = popStyle(v)
            w = makeWidget(parent, propObj, k, t, v)
            if not isPage(w):
                addToParent(parent=parent, widget=w, style=style)
            layoutFrom(w)
            if isContainerKey(k):
                if type(v) is list:
                    layout(w, v, propObj)
    parent.Layout()
    return parent


def buildGUI(buildSpec, propObj):
    """
    build a GUI from a build spec dictionary (or JSON)
    """
    checkSpec(buildSpec)
    mainWin = wx.Frame(None)
    mainWin.statusbar = mainWin.CreateStatusBar(1)
    updateStatus()

    mainWin.SetTitle(buildSpec['appName'])
    mainWin.SetSize((buildSpec['windowSize']['width'], buildSpec['windowSize']['height']))

    mainSizer = wx.BoxSizer(wx.VERTICAL)
    mainWin.SetSizer(mainSizer)
    mainWin = layout(mainWin, buildSpec['layout'], propObj)
    
    mainWin.Fit()
    mainWin.Centre()
    mainWin.Show()
    return mainWin







