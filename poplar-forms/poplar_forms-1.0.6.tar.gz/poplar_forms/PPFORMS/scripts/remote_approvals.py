###############################################################################
#  expip - Python Package Manager for Orchid Extender
#
#  expip is the Python package manager for Orchid Extender.  It enables you to
#  take advantage of the Python ecosystem.  Use it to install any package from
#  pypi.org or expi.dev.
#
#  author: Chris Binckly (2665093 Ontario Inc.)
#  email: cbinckly@gmail.com
#  Copyright 2665093 Ontario Inc. 2019
#
#  This software has a non-exclusive license and cannot be sublicensed, reused,
#  transferred or modified without written consent from 2665093 Ontario Inc.
#
###############################################################################
import os
import re
import sys
import bz2
import json
import base64
import string
import random
import hashlib
import datetime
import requests
import tempfile
import platform
import traceback
import subprocess
import configparser
from pathlib import Path
from contextlib import contextmanager

from accpac import *

from form_client import NamespaceClient

DEBUG = False
NAME = "expip - Python Package Manager for Extender"
VERSION = "2.2.3"

BILLING_EMAIL = "cbinckly@gmail.com"
SUPPORT_EMAIL = "cbinckly@gmail.com"
SUPPORT_URL = "https://2665093.ca"

PYSIG = "https://expi.dev/python/{version}/{file}"
UPDSIG = "https://expi.dev/access"
SHAS = { "3.4.2": {
            "python.exe": "8113c872d18c3f19aafc8c0e3bb4c3d94990f5cc2562b2c8654a6972e012f776",
            "python34.dll": "ea8d834c3f7f69270e47fbcccf9a159385b39b4aa7c6aae4a28fa9ff835455a7",
            },
       }

SCHEME_RE = re.compile(r'^(\w+)(\+(\w+)|)://')
PKG_FROM_SCHEME_RE = re.compile(r'/([a-zA-z0-9\-_])(.git|)[@#].+$')

MODULE = "EXPIP"
TABLE = "EXPIPCON"

PIPMIN = 19
PIPMAX = 20

## Entry point

def main(args):
    RemoteApprovalsUI()

### Utility Functions

def _debug(msg, excinfo=None):
    if DEBUG:
        msg = "DEBUG {}\n{}\n---------\n{}".format(rotoID, NAME, msg)
        if excinfo:
            msg = "\n".join([msg, traceback.format_exc(), ])
        showMessageBox(msg)

def _alert(msg):
    showMessageBox("{}\n\n{}".format(NAME, msg))

def success(*args):
    if sum(args) > 0:
        return False
    return True

### Interface Definition

class RemoteApprovalsUI(UI):
    """UI for Remote approvals management.    """

    # Custom control constants
    BUTTON_WIDTH = 1265
    BUTTON_SPACE = 150

    # Grid layout
    COL_MONTH = 0
    COL_USAGE = 1

    def __init__(self):
        """Initialize a new UI instance.  Speaks."""
        UI.__init__(self)
        

        shown = False
        try:
            self.namespace_client = NamespaceClient()
            self.namespaces = self.namespace_client.list()
            self.namespace = self.namespaces[0]
            self.title = "Remote Approval Management - {}".format(
            self.namespace['subdomain'])
            self.createScreen()
            self.show()
            shown = True
            self._refresh_grid()
        except Exception as e:
            if not shown:
                self.show()
            _alert("Error starting up: {}".format(
                e))
            _debug(e, excinfo=sys.exc_info()[2])
            self.closeUI()
        else:
            self.onClose = self.onCloseClick

    # Requests

    def createScreen(self):
        """Configure and render the fields and buttons.
        | Namespace subdomain.ff.io             |
        |                                       |
        | Soft Limit: NNNNNNNN                  |
        | Hard Limit: NNNNNNNN                  |
        |                                       |
        | Remaining this Month: NNNNNN          |
        |                                       |
        || Period   |                  Usage   ||
        || 2019-12  |                  15456   ||
        || 2020-01  |                  16765   ||
        |                                       |
        |  Logo: [https://path/logo.png       ] |
        | Style: [https://path/style.png      ] |
        |                                       |
        |                    +Save      +Close  |

        """



        f = self.addUIField("namespaceLabel")
        f.controlType = "EDIT"
        f.size = 250
        f.width = 5000
        f.labelWidth = 60
        f.caption = "Namespace"
        f.hasFinder = False
        f.setValue("{}.fleetingforms.io".format(self.namespace['subdomain']))
        f.enabled = False
        self.namespace_field = f

        f = self.addUIField("softLimitLabel")
        f.controlType = "EDIT"
        f.size = 250
        f.width = 5000
        f.labelWidth = 60
        f.caption = "Soft Limit"
        f.hasFinder = False
        f.setValue(str(self.namespace['soft_limit']))
        f.enabled = False
        self.soft_limit_field = f
        
        f = self.addUIField("hardLimitLabel")
        f.controlType = "EDIT"
        f.size = 250
        f.width = 5000
        f.labelWidth = 60
        f.caption = "Hard Limit"
        f.hasFinder = False
        f.setValue(str(self.namespace['hard_limit']))
        f.enabled = False
        self.hard_limit_field = f


        f = self.addUIField("remainingLabel")
        f.controlType = "EDIT"
        f.size = 250
        f.width = 5000
        f.labelWidth = 60
        f.caption = "Remaining (Month)"
        f.hasFinder = False
        curmonth = datetime.datetime.now().strftime("%Y-%m")
        f.enabled = False
        f.setValue(str(self.namespace['soft_limit'] - 
                   self.namespace['usage'].get(curmonth, 0)))
        self.remaining_field = f

        f = self.addUIField("supportEmailField")
        f.controlType = "EDIT"
        f.size = 250
        f.width = 5000
        f.labelWidth = 60
        f.caption = "Support Email"
        f.setValue(self.namespace.get('support_email', ''))
        f.hasFinder = False
        self.support_email_field = f
        
        f = self.addUIField("logoUrlField")
        f.controlType = "EDIT"
        f.size = 250
        f.width = 5000
        f.labelWidth = 60
        f.caption = "Logo URL"
        f.setValue(self.namespace.get('logo', ''))
        f.hasFinder = False
        self.logo_field = f

        f = self.addUIField("styleUrlField")
        f.controlType = "EDIT"
        f.size = 250
        f.width = 5000
        f.labelWidth = 60
        f.caption = "Style URL"
        f.setValue(self.namespace.get('style', ''))
        f.hasFinder = False
        self.style_field = f

        grid = self.addGrid("usageGrid")

        grid.setOnBeginEdit(self.gridOnBeginEdit)
        grid.onRowChanged = self.gridOnRowChanged

        grid.height = -100
        grid.width = -150
        # grid.top = self.remaining_label.top + 150
        grid.addTextColumn("Month", "LEFT", 100, True)
        grid.addTextColumn("Approvals", "Right", 300, True)
        self.usage_grid = grid
        self.usage_grid.removeAllRows()

        btn = self.addButton("btnSave", "&Save")
        btn.top = - self.BUTTON_SPACE - btn.height
        btn.width = self.BUTTON_WIDTH
        btn.left = self.usage_grid.left
        btn.onClick = self.onSaveClick
        self.btnSave = btn
        
        btn = self.addButton("btnClose", "&Close")
        btn.top = - self.BUTTON_SPACE - btn.height
        btn.width = self.BUTTON_WIDTH
        btn.left = -self.BUTTON_SPACE - self.BUTTON_WIDTH
        btn.onClick = self.onCloseClick
        self.btnClose = btn

        self.usage_grid.height = -self.BUTTON_SPACE - btn.height - 75

    def gridOnBeginEdit(self, e):
        _alert("Items in this grid cannot be edited.")
        return Abort

    def gridOnRowChanged(self, new_row):
        return Continue

    def _refresh_grid(self):
        for month, usage in self.namespace['usage'].items():
            row = self.usage_grid.createRow()
            row.columns[self.COL_MONTH] = month
            row.columns[self.COL_USAGE] = str(usage)
            self.usage_grid.addRow(row)

    # Event Handling
    def onSaveClick(self):
        if not hasattr(self, 'namespace') or not self.namespace:
            return Continue
            
        logo = self.logo_field.getValue()
        style = self.style_field.getValue()
        support_email = self.support_email_field.getValue()
        
        data = {
            'id': self.namespace['id'],
            'subdomain': self.namespace['subdomain'],
            'support_email': support_email,
            'logo': logo,
            'style': style,
        }
        
        try:
            self.namespace_client.update(self.namespace['id'], 
                                         data=data)
            _alert("Remote approvals settings updated.")
        except Exception as e:
            _alert("Remote approval settings update failed: {}".format(e))
        
        return Continue
            

    def onCloseClick(self):
        """Close the UI if the Close button or window X are clicked."""
        self.closeUI()
