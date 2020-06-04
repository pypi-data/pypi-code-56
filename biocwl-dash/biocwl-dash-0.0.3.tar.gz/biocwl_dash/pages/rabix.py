import glob
import json
import os

import yaml
import dash_html_components as html
import flask
import dash_rabix

from ..utils import Header, RABIX_PATH, wrapInHeader


def create_layout(app, base_url, report_service, workflow_path):
    workflow_contents_obj = report_service.getCwl()
    workflow_contents_json = json.dumps(workflow_contents_obj)

    return wrapInHeader(
        app,
        base_url,
        report_service,
        [
            html.H6(
                ["Rendering workflow"],
                className="subtitle padded",
            ),
            dash_rabix.DashRabix(
                cwlWorkflow=workflow_contents_json,
                style={"width": 700, "height": 750,},
                showHeader=False,
            ),
        ],
    )

