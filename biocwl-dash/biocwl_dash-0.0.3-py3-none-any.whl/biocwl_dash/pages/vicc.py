import base64
import io
import glob
import os

import dash
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import csv
import plotly.graph_objects as go
import plotly.express as px

from ..utils import make_dash_table, wrapInHeader


def plot_pie(df, column_name):
    labels = df[column_name].value_counts().index
    values = df[column_name].value_counts().values
    # Use `hole` to create a donut-like pie chart
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3, title=column_name)])
    fig.update_layout(
        showlegend=False,
        autosize=True,
        margin=dict(t=0, l=0, r=0, b=0),
    )
    return fig


def plot_sunburst(df):
    values_sum = df.groupby(['VICC Evidence Label']).size()
    values = df.groupby(['VICC Evidence Label', 'VICC Evidence Description']).size().reset_index(name='counts')
    parent = (values['VICC Evidence Label'].tolist())
    character = (values['VICC Evidence Description'].tolist())
    values = (values['counts'].tolist())

    #### Adding to overcome "implied roots, cannot build sunburst hierarchy."
    values = [
        values_sum.get('A', 0),
        values_sum.get('B', 0),
        values_sum.get('C', 0),
        values_sum.get('D', 0)
    ] + values
    for i, item in enumerate(character):
        if isinstance(item, str):
            num_of_words = len(item.split(' '))
            if num_of_words > 2:
                character[i] = item.rsplit(' ')[0] + ' ' + item.rsplit(' ')[1]

    parent = [None, None, None, None] + parent
    character = ['A', 'B', 'C', 'D'] + character
    data = dict(
        character=character,
        parent=parent,
        value=values)

    fig = go.Figure(px.sunburst(
        data,
        names='character',
        parents='parent',
        values='value',
    ))
    fig.update_layout(width=700, height=900, margin = dict(t=0, l=0, r=0, b=0))
    return fig


def create_layout(app, base_url, report_service):
    vic_path = [f for f in report_service.getSecondaryFiles() if f.endswith('vicc_maf.csv')]

    if not vic_path:
        return wrapInHeader(
            app, base_url, report_service,
            html.H6(
                "No vicc_maf file found.", className="subtitle padded"
            )
        )

    vic_path = vic_path[0]
    df_vicc = pd.read_csv(
        report_service.openSecondaryFile(vic_path),
        index_col=False,
        quoting=csv.QUOTE_NONNUMERIC
    )
    fig1 = plot_pie(df_vicc, 'VICC Evidence Label')
    fig2 = plot_pie(df_vicc, 'VICC Evidence Description')
    sunburst = plot_sunburst(df_vicc)

    return wrapInHeader(app, base_url, report_service,
        [
            html.Div(
                [
                    html.Div(
                        [
                            html.H6(
                                ["VICC"], className="subtitle padded"
                            ),
                            html.P(
                                [
                                    f"This page will summarize findings from The Variant Interpretation for Cancer Consortium (VICC) {report_service.getReportId()}."
                                ],
                                style={"color": "#7a7a7a"},
                            ),
                        ],
                        className="twelve columns",
                    )
                ],
                className="row ",
            ),
            # Row 2
            html.Div(
                [
                    html.Div(
                        [
                            html.Br([]),
                            html.H6(
                                ["VICC Table"],
                                className="subtitle tiny-header padded",
                            ),
                            html.Div(
                                [
                                    html.Table(
                                        make_dash_table(df_vicc),
                                        className="tiny-header",
                                    )
                                ],
                                style={"margin": "0px"},
                            ),
                        ],
                        className="twelve columns",
                    )
                ],
                className="row ",
            ),
            # Row 3
            html.Div(
                [
                    html.Div(
                        [
                            html.Br([]),
                            html.H6(
                                ["VICC Variant Classification Distribution"],
                                className="subtitle tiny-header padded",
                            ),
                            # html.Div([
                            #     html.Div([
                            #         dcc.Graph(id='g1', style={'height': 250}, figure=sunburst, responsive=True)
                            #     ], className="six columns"),
                            #
                            # ], className="row")
                            html.Div([dcc.Graph(figure=sunburst, style={'height': 250}, responsive=True)]),
                        ],
                        className="twelve columns",
                    )
                ],
                className="row ",
                style={'height': '100%'},
            ),
        ])
