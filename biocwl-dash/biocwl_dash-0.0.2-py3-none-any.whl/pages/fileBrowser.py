import os

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import dash_lazylog
import pandas
import pathlib
import plotly.graph_objs as go

from ..utils import wrapInHeader, FILE_BROWSER_PATH, RABIX_PATH


def create_layout(app, base_url, report_service, subpath):
  return wrapInHeader(
    app,
    base_url,
    report_service,
    [
      html.H6(
        html.A(
          'View Primary Files in Arvados',
          href=report_service.getLinkToPrimaryFiles()
        )
      ),
      html.H6(
        html.A(
          'View Merge Files in Arvados',
          href=report_service.getLinkToMergeFiles()
        )
      ),
      html.H6(
        html.A(
          'View Secondary Files in Arvados',
          href=report_service.getLinkToSecondaryFiles()
        )
      ),
    ],
  )