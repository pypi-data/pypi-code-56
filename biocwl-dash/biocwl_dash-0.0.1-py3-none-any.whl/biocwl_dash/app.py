"""BioCwl Dash app.

Initial version copied directly from github:
https://github.com/plotly/dash-sample-apps/blob/04b946a0363c9b28caff846b3b35304d2bd3bb39/apps/biocwl-dash-report/app.py
"""

import os
import time

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from flask import current_app
from werkzeug.exceptions import BadRequest


from .pages import fileBrowser, rabix, overview, copyNumberVariation, expression, geneFusions, vicc
from .utils import FILE_BROWSER_PATH, RABIX_PATH


def init_app(server, prefix, report_service_factory):
    """Add the BioCwl Dash app to the provided Flask server.

    Args:
      server: a flask server
      prefix: the URL prefix for this app (eg: /dash/)
      report_service_factory: an implementation of ReportServiceFactory
    """
    app = dash.Dash(
        __name__,
        meta_tags=[{"name": "viewport", "content": "width=device-width"}],
        server=server,
        url_base_pathname=prefix,
    )

    # Necessary because we have dynamic layouts and add callbacks in this page (referencing inputs
    # and outputs which don't exist).
    app.config.suppress_callback_exceptions = True

    # Describe the layout / UI of the app
    app.layout = html.Div(
        [
            dcc.Location(id="url", refresh=False),
            html.Div(
                [
                    dcc.Loading(id="load", children=[html.Div(id="page-content")], type="default")
                ],
                className="page"
            )
        ]
    )

    # Update page
    @app.callback(Output("page-content", "children"), [Input("url", "pathname")])
    def display_page(pathname):
        if pathname and pathname.startswith(prefix):
            pathname = pathname[len(prefix) :]

        # reports.url.com/: View all reports.
        if not pathname:
            return html.Div("No report ID provided.")
        components = pathname.split("/")
        report_id = components.pop(0)
        try:
            report_service = report_service_factory.getReportService(report_id)
        except BadRequest as e:
            return html.Div(str(e))

        # reports.url.com/<report_id>: Landing page for report.
        if not components:
            return overview.create_layout(
                app, prefix, report_service, report_service_factory
            )
        report_page = components.pop(0)

        # reports.url.com/<report_id>/files[/sub/path]: View files within report.
        if report_page == FILE_BROWSER_PATH:
            return fileBrowser.create_layout(
                app, prefix, report_service, "/".join(components)
            )
        # reports.url.com/<report_id>/rabix: Workflow renderer.
        elif report_page == RABIX_PATH:
            return rabix.create_layout(
                app, prefix, report_service, "/".join(components)
            )
        # reports.url.com/<report_id>/*: All other pages.
        elif report_page == "gene-fusions":
            return geneFusions.create_layout(app, prefix, report_service)
        elif report_page == "copy-number-variation":
            return copyNumberVariation.create_layout(app, prefix, report_service)
        elif report_page == "expression":
            return expression.create_layout(app, prefix, report_service)
        elif report_page == "vicc":
            return vicc.create_layout(app, prefix, report_service)
        elif report_page == "full-view":
            return (
                overview.create_layout(
                    app, prefix, report_service, report_service_factory
                ),
                copyNumberVariation.create_layout(app, prefix, report_service),
                geneFusions.create_layout(app, prefix, report_service),
                expression.create_layout(app, prefix, report_service),
                vicc.create_layout(app, prefix, report_service),
            )
        else:
            return overview.create_layout(
                app, prefix, report_service, report_service_factory
            )

    # This handles image selection on the gene-fusions page.
    #
    # TODO: We figure out a way to move page logic into the page in the future.
    @app.callback(
        dash.dependencies.Output("gene-fusions-image", "src"),
        [dash.dependencies.Input("gene-fusions-image-dropdown", "value")],
    )
    def update_gene_fusions_image_src(value):
        return value

    @app.callback(
        dash.dependencies.Output("file-browser-input-value", "children"),
        [dash.dependencies.Input("file-browser-input", "value")],
        [dash.dependencies.State("file-browser-fcontents-hidden", "children")],
    )
    def update_file_browser_input(search_term, fcontents):
        if search_term:
            filtered = [
                line
                for line in fcontents.split("\n")
                if (search_term.lower() in line.lower())
            ]
            return "\n".join(filtered)
        return fcontents

    return app
