import os

import dash_html_components as html
import dash_core_components as dcc
import dash_table

FILE_BROWSER_PATH = "files"
RABIX_PATH = "rabix"


def Header(app, base_url, report_service):
    return html.Div(
        [
            get_header(app, base_url, report_service),
            html.Br([]),
            get_menu(base_url, report_service),
        ]
    )


def get_header(app, base_url, report_service):
    report_id = report_service.getReportId()
    header = html.Div(
        [
            html.Div(
                [
                    html.Img(src=app.get_asset_url("mssm-logo.png"), className="logo",),
                    # html.A(
                    #     html.Button("All Reports", id="learn-more-button"),
                    #     href="/",
                    # ),
                ],
                className="row",
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.H5(
                                f"Report for {report_service.getPatientName()} T{report_service.getReportNumber()}"
                            )
                        ],
                        className="nine columns main-title",
                    ),
                    html.Div(
                        [
                            dcc.Link(
                                "Full View",
                                href=f"{base_url}{report_id}/full-view",
                                className="full-view-link",
                            )
                        ],
                        className="three columns",
                    ),
                ],
                className="twelve columns",
                style={"padding-left": "0"},
            ),
        ],
        className="row",
    )
    return header


def get_menu(base_url, report_service):
    report_id = report_service.getReportId()
    menu = html.Div(
        [
            dcc.Link(
                "Overview",
                href=f"{base_url}{report_id}/overview",
                className="tab first",
            ),
            dcc.Link(
                "CNA",
                href=f"{base_url}{report_id}/copy-number-variation",
                className="tab",
            ),
            dcc.Link(
                "Gene Fusions",
                href=f"{base_url}{report_id}/gene-fusions",
                className="tab",
            ),
            dcc.Link("Expression", href=f"{base_url}{report_id}/expression", className="tab",),
            dcc.Link("VICC", href=f"{base_url}{report_id}/vicc", className="tab",),
            dcc.Link(
                "Workflow", href=f"{base_url}{report_id}/{RABIX_PATH}", className="tab",
            ),
            dcc.Link(
                "Files",
                href=f"{base_url}{report_id}/{FILE_BROWSER_PATH}",
                className="tab",
            ),
        ],
        className="row all-tabs",
    )
    return menu


def make_dash_table(df):
    """ Return a Dash DataTable for a Pandas dataframe """
    table = dash_table.DataTable(
        id="table",
        virtualization=True,
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict("records"),
        fixed_columns={"headers": True, "data": 0},
        sort_action="native",
        sort_mode="multi",
        page_action="native",
        page_current=0,
        page_size=10,
        style_table={
            "minHeight": "300px",
            "height": "300px",
            "maxHeight": "300px",
            "minWidth": "600px",
            "width": "600px",
            "maxWidth": "600px",
            "overflowY": "scroll",
            "overflowX": "scroll",
            "border": "thin lightgrey solid",
        },
        style_cell={
            # all three widths are needed
            "minWidth": "0px",
            "maxWidth": "180px",
            "overflow": "scroll",
        },
    )
    return table


def getLinkToReport(base_url, report_service):
    return f"{base_url}{report_service.getReportId()}"


def wrapInHeader(app, base_url, report_service, contents):
    return html.Div(
        [
            Header(app, base_url, report_service),
            html.Div(
                [
                    # Row 1
                    html.Div(contents),
                ],
                className="sub_page",
            ),
        ],
    )
