"""
the widges module provides common widgets that are intended
to be embedded within other FSL guis.  
"""
import os
import subprocess

import wx
import fsleyes
import fsleyes.overlay as fsloverlay
import fsleyes.displaycontext as fsldc
import fsleyes.views.orthopanel as orthopanel
import fsleyes.profiles as profiles
import fsleyes.profiles.profilemap as profilemap
import fsleyes.colourmaps as colourmaps
import fsleyes_props as props
from fsleyes.main import embed

from fsl.utils.platform import platform as fslplatform
from fsl.utils import idle
import fsl.data.image as fslimage

import fsl.gui.icons as fslicons
import fsl.gui.exceptions as fslerrs
props.initGUI()

class column(wx.Panel):
    """
    a wx.Panel with a vertical sizer
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.SetSizer(wx.BoxSizer(wx.VERTICAL))
        # self.SetBackgroundColour((0, 255, 0))

class row(wx.Panel):
    """
    a wx.Panel with a horizontal sizer
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.SetSizer(wx.BoxSizer(wx.HORIZONTAL))
        # self.SetBackgroundColour((255, 0, 0))

def button(parent, propobj, **kwargs):
    if kwargs.get('label') == None:
        raise fslerrs.MissingRequiredKey("A 'label' key is required")
    if kwargs.get('propName') == None:
        raise fslerrs.MissingRequiredKey("A 'propName' key is required")
    btn = props.build._createButton(parent, getattr(propobj, kwargs['propName']), propobj, parent)
    return btn


def group(parent, label):
    """
    Uses a wx.StaticBoxSizer to group items visually
    """
    panel = wx.Panel(parent)
    bsizer = wx.StaticBoxSizer(wx.VERTICAL, panel, label)
    panel.SetSizer(bsizer)
    return panel

def notebook(parent):
    """
    noetbook
    """
    notebook = wx.Notebook(parent)
    return notebook

def page(parent):
    """
    page
    """
    panel = wx.Panel(parent)
    sizer = wx.BoxSizer(wx.VERTICAL)
    panel.SetSizer(sizer)
    panel.SetBackgroundColour(wx.NullColour)
    return panel

def filepath(parent, propobj, **kwargs):
    if kwargs.get('label') == None:
        raise fslerrs.MissingRequiredKey("A 'label' key must be provided to a FilePath")
    panel = wx.Panel(parent)
    panel.SetSizer(wx.BoxSizer(wx.HORIZONTAL))
    st = wx.StaticText(panel, label=kwargs['label'])
    panel.GetSizer().Add(st, proportion=0, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=2)
    f = props.widgets.makeWidget(panel, propobj, kwargs['propName'])
    panel.GetSizer().Add(f, proportion=1, flag=wx.ALL | wx.EXPAND, border=5)
    return panel


def checkbox(parent, propobj, **kwargs):
    if kwargs.get('label') == None:
        raise fslerrs.MissingRequiredKey("A 'label' key must be provided to a Checkbox")
    panel = wx.Panel(parent)
    panel.SetSizer(wx.BoxSizer(wx.HORIZONTAL))
    st = wx.StaticText(panel, label=kwargs['label'])
    panel.GetSizer().Add(st, proportion=0, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=2)
    ch = props.widgets.makeWidget(panel, propobj, kwargs['propName'])
    panel.GetSizer().Add(ch, proportion=0, flag=wx.ALL | wx.EXPAND, border=5)
    return panel

def number(parent, propobj, **kwargs):
    if kwargs.get('label') == None:
        raise fslerrs.MissingRequiredKey("A 'label' key must be provided to a Checkbox")
    panel = wx.Panel(parent)
    panel.SetSizer(wx.BoxSizer(wx.HORIZONTAL))
    st = wx.StaticText(panel, label=kwargs.pop('label'))
    panel.GetSizer().Add(st, proportion=0, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=2)
    prp = props.widgets.makeWidget(panel, propobj, **kwargs)
    panel.GetSizer().Add(prp, proportion=0, flag=wx.ALL | wx.EXPAND, border=5)
    return panel

def point(parent, propobj, **kwargs):
    if kwargs.get('label') == None:
        raise fslerrs.MissingRequiredKey("A 'label' key must be provided to a Checkbox")
    panel = wx.Panel(parent)
    panel.SetSizer(wx.BoxSizer(wx.HORIZONTAL))
    st = wx.StaticText(panel, label=kwargs.pop('label'))
    panel.GetSizer().Add(st, proportion=0, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=2)
    prp = props.widgets.makeWidget(panel, propobj, **kwargs)
    panel.GetSizer().Add(prp, proportion=0, flag=wx.ALL | wx.EXPAND, border=5)
    return panel

def choice(parent, propobj, **kwargs):
    if kwargs.get('label') == None:
        raise fslerrs.MissingRequiredKey("A 'label' key must be provided to a Checkbox")
    panel = wx.Panel(parent)
    panel.SetSizer(wx.BoxSizer(wx.HORIZONTAL))
    st = wx.StaticText(panel, label=kwargs['label'])
    panel.GetSizer().Add(st, proportion=0, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=2)
    prp = props.widgets.makeWidget(panel, propobj, kwargs['propName'])
    panel.GetSizer().Add(prp, proportion=0, flag=wx.ALL | wx.EXPAND, border=5)
    return panel


class ViewProfile(profiles.Profile):
    def __init__(self, viewPanel, overlayList, displayCtx):
        profiles.Profile.__init__(self,
                                  viewPanel,
                                  overlayList,
                                  displayCtx,
                                  ['nav'])

    def getEventTargets(self):
        return [self.viewPanel.getXCanvas(),
                self.viewPanel.getYCanvas(),
                self.viewPanel.getZCanvas()]

    def _navModeLeftMouseDrag(self, ev, canvas, mousePos, canvasPos):
        if canvasPos is None:
            return False
        self.displayCtx.location = canvasPos
        return True


# This is the hacky bit - there is
# currently no formal way to register
# a custom profile class with a view.
# This might change in the future.

# The first profile in the profiles
# list is used as the default.
profilemap.profiles[orthopanel.OrthoPanel].insert(0, 'minview')
profilemap.profileHandlers[orthopanel.OrthoPanel, 'minview'] = ViewProfile

class FsleyesImage(wx.Panel):
    def __init__(self, parent, propobj, **kwargs):
        super().__init__(parent, **kwargs)
        self.overlayList, masterDisplayCtx, _ = embed(None, mkFrame=False)
        self.displayCtx = fsldc.DisplayContext(self.overlayList, parent=masterDisplayCtx)

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.op = orthopanel.OrthoPanel(
                self,
                self.overlayList,
                self.displayCtx,
                None)
        self.op.SetMinSize((-1, 300))
        self.op.Show()

        self.btn_fsleyes = wx.Button(self, label="Open in FSLeyes")
        sizer.Add(self.btn_fsleyes, proportion=0, flag=wx.ALL, border=5)
        sizer.Add(self.op, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)
        self.SetSizer(sizer)

        # bind events
        self.btn_fsleyes.Bind(wx.EVT_BUTTON, self.launch_fsleyes)
        propobj.addListener('inputFile', 'FsleyesListener', self.add_image)
    
    def _run_fsleyes(self):
        imgs = [img.dataSource for img in self.overlayList]
        # print([img.dataSource for img in self.overlayList])
        cmd = [
            os.path.join(fslplatform.fsldir, 'bin', 'fsleyes'),
            " ".join(imgs)
        ]
        subprocess.run(
            " ".join(cmd),
            shell=True, 
            check=True
        )


    def launch_fsleyes(self, event):
        thread_id = idle.run(self._run_fsleyes)

    def reset(self):
        self.overlayList.clear()

    def add_image(self, new_img, valid, context, name):
        self.reset()
        img = fslimage.Image(new_img)
        self.overlayList.append(img)

    def add_mask(self, new_img):
        img = fslimage.Image(new_img)
        self.overlayList.append(img, cmap='red', alpha=30)
