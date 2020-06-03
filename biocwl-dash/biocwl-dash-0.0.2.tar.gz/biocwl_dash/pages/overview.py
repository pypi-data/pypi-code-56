import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import numpy
import re
import dash_table
import pandas as pd
import pathlib

from ..utils import wrapInHeader, getLinkToReport


DATE_STR_FMT = "%m/%d/%Y"

def getGep70OrMsg(report_service):
    """Returns GEP70 or error msg."""
    gep70_tsvs = [f for f in report_service.getSecondaryFiles() if re.match(r'gep70scores.*\.csv', f)]
    if not gep70_tsvs:
        return 'No scores found'
    scores = pd.read_csv(
        report_service.openSecondaryFile(gep70_tsvs[0], 'r'),
        skiprows=1,
        names=['run', 'score'],
        sep='\t'
    )

    matching = scores.apply(lambda r: report_service.reportIdsAreEquivalent(r.run), axis=1)
    matches = scores[matching]
    if matches.shape[0] == 0:
        return f'{report_service.getReportId()} not found'
    return float(matches.iloc[0].score)


def create_layout(app, base_url, report_service, report_service_factory):
    df_patient_background = pd.DataFrame(
        [
            ["MRN", report_service.getPatientMrn()],
            ["Name", report_service.getPatientName()],
            ["Date of Birth", report_service.getPatientDob()],
            ["Sex", report_service.getPatientSex()],
            ["Tumor Sample Date", report_service.getTumorSampleDate().strftime(DATE_STR_FMT)],
            ["Normal Sample Date", report_service.getNormalSampleDate().strftime(DATE_STR_FMT)],
        ]
    )

    gep70 = getGep70OrMsg(report_service)

    # Make a DF with one row per patient report and many helpful columns.
    all_reports = pd.DataFrame({'report_id': report_service.getAllPatientReportIds()})
    all_reports['report_service'] = all_reports['report_id'].apply(report_service_factory.getReportService)
    all_reports['report_link'] = all_reports['report_service'].apply(
        lambda rs: f'[{rs.getReportId()}]({getLinkToReport(base_url, rs)})')
    all_reports['tumor_date'] = all_reports['report_service'].apply(lambda rs: rs.getTumorSampleDate())
    all_reports['tumor_date_str'] = all_reports['tumor_date'].apply(lambda d: d.strftime(DATE_STR_FMT))
    all_reports['gep70'] = all_reports['report_service'].apply(lambda rs: getGep70OrMsg(rs))
    all_reports['gep70_str'] = all_reports['gep70'].apply(lambda scr: scr if type(scr) == str else ('%.1f' % scr))

    # Page layouts
    return wrapInHeader(
        app,
        base_url,
        report_service,
        [
            # Row 3
            html.Div(
                [
                    html.Div(
                        [
                            html.H5(
                                "Multiple Myeloma Personalized Medicine Report"
                            ),
                        ],
                        className="product",
                    )
                ],
                className="row",
            ),
            # Row 4
            html.Div(
                [
                    html.Div(
                        [
                            html.H6(
                                ["Patient Background"], className="subtitle padded"
                            ),
                            dash_table.DataTable(
                                columns=[{ 'name': False, 'id': c, 'presentation': 'markdown'} for c in df_patient_background.columns],
                                data=df_patient_background.to_dict('records'),
                                row_selectable=False,
                            ),
                            html.H6(
                                ["Other Reports"], className="subtitle padded"
                            ),
                            dash_table.DataTable(
                                columns=[{
                                    'name': 'Report',
                                    'id': 'report_link',
                                    'presentation': 'markdown'
                                }, {
                                    'name': 'Date',
                                    'id': 'tumor_date_str',
                                    'presentation': 'markdown',
                                }, {
                                    'name': 'GEP 70',
                                    'id': 'gep70_str',
                                }],
                                data=all_reports[['report_link', 'tumor_date_str', 'gep70_str']].to_dict('records'),
                                row_selectable=False,
                            )
                        ],
                        className="six columns",
                    ),
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        "GEP70 Score", className="subtitle padded",
                                    ),
                                    dcc.Graph(
                                        id="graph-2",
                                        figure={
                                            "data": [
                                                go.Indicator(
                                                    mode = "number",
                                                    value = gep70 if type(gep70) != str else numpy.NAN,
                                                    gauge = {'axis': {'range': [0, 100]}}
                                                )
                                            ],
                                            "layout": go.Layout(
                                                autosize=False,
                                                title="",
                                                #font={"family": "Raleway", "size": 10},
                                                height=130,
                                                width=340,
                                                margin={
                                                    "r": 0,
                                                    "t": 20,
                                                    "b": 10,
                                                    "l": 10,
                                                },
                                            ),
                                        },
                                    ),
                                    html.H6(gep70 if type(gep70) == str else ''),
                                ],
                                style={"margin-bottom": "35px"},
                            ),
                            dcc.Graph(
                                id="graph-2",
                                figure={
                                    "data": [
                                        go.Scatter(
                                            x=all_reports.tumor_date,  # .apply(lambda r: r.strftime("%m/%d/%Y"))
                                            y=all_reports.gep70,
                                            line={"color": "#97151c"},
                                            mode="lines+markers",
                                            name="GEP70 Score",
                                        )
                                    ],
                                    "layout": go.Layout(
                                        autosize=True,
                                        title="",
                                        font={"family": "Raleway", "size": 10},
                                        height=200,
                                        width=340,
                                        hovermode="closest",
                                        legend={
                                            "x": -0.0277108433735,
                                            "y": -0.142606516291,
                                            "orientation": "h",
                                        },
                                        margin={
                                            "r": 20,
                                            "t": 20,
                                            "b": 20,
                                            "l": 50,
                                        },
                                        showlegend=True,
                                        xaxis={
                                            "showgrid": False,
                                            "showline": True,
                                            "title": "",
                                        },
                                        yaxis={
                                            "nticks": 4,
                                            "range": [0, 100],
                                            "showgrid": True,
                                            "showline": True,
                                            "ticklen": 10,
                                            "ticks": "outside",
                                            "title": "GEP70",
                                        },
                                    ),
                                },
                                config={"displayModeBar": False},
                            ),
                        ],
                        className="six columns",
                    ),
                ],
                className="row",
                style={"margin-bottom": "35px"},
            ),
        ]
    )
