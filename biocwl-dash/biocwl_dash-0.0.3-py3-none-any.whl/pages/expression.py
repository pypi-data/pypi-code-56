import base64
import io
import glob
import os

import dash
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import numpy
from pdf2image import convert_from_bytes
import plotly.graph_objs as go

from ..utils import Header, make_dash_table, wrapInHeader


ZSCORE_FILE = 'zscores_latest.csv'
CORRECTED_COUNTS_FILE = 'normCorrCounts_voom_thr1_latest.csv'


def getBlueRedLinePlot(values, title, report_id, ylabel):
    """Plots a line graph for values, coloring <0 blue and >0 red.

    Args:
      values: pandas.Series, sorted, with an index of report_ids
      title: plot title
      report_id: report id
    """
    first_zero = (values > 0).idxmax()
    plt_left = go.Scatter(
        x=values[:first_zero].index,
        y=values[:first_zero],
        mode='lines',
        fill='tozeroy',
        fillcolor='skyblue',
        name='zscore'
    )
    plt_right = go.Scatter(
        x=values[first_zero:].index,
        y=values[first_zero:],
        mode='lines',
        fill='tozeroy',
        fillcolor='firebrick',
        name='zscore'
    )

    return dcc.Graph(
        figure={
            "data": [plt_left, plt_right],
            "layout": go.Layout(
                title=title,
                yaxis_title=ylabel,
                xaxis_title="Patients",
                showlegend=False,
                margin={
                    "r": 30,
                    "t": 40,
                    "b": 100,
                    "l": 50,
                },
                height=300,
                hovermode="x unified",
                xaxis=dict(
                    showline=False,
                    showgrid=False,
                    showticklabels=False,
                    linecolor='rgb(204, 204, 204)',
                ),
                yaxis=dict(
                    dtick=1.0
                ),
                shapes=[
                    dict(
                        type='line',
                        yref='y',
                        y0=0,
                        y1=values[report_id],
                        xref='x',
                        x0=report_id,
                        x1=report_id
                    )
                ]
            )
        }
    )


def getPlotForZscore(zscores, gene, report_id, aka=None):
    if not (zscores.Gene == gene).any():
        return html.Div(f'Expression for gene {gene} not found.')
    if not report_id in zscores.columns:
        return html.Div(f'No zscore for {report_id}: {zscores.columns}')

    gene_scores = zscores.set_index('Gene').loc[gene].sort_values()

    if aka:
        title = f'{aka} Expression ({gene})'
    else:
        title = f'{gene} Expression'

    return getBlueRedLinePlot(gene_scores, title, report_id, ylabel='Gene Expression [z-score]')


def getPlotForGeneRatio(corrected_counts, gene1, gene2, gene_mapping, report_id):
    ensg_ids1 = gene_mapping[gene_mapping == gene1]
    ensg_ids2 = gene_mapping[gene_mapping == gene2]
    if not ensg_ids1.shape[0]:
        return html.Div(f'Could not find the ENSG ID for gene {gene1}')
    if not ensg_ids2.shape[0]:
        return html.Div(f'Could not find the ENSG ID for gene {gene2}')
    ensg_id1 = ensg_ids1.index[0]
    ensg_id2 = ensg_ids2.index[0]

    if not (corrected_counts.index == ensg_id1).any():
        return html.Div(f'Expression for gene {ensg_id1} not found.')
    if not (corrected_counts.index == ensg_id2).any():
        return html.Div(f'Expression for gene {ensg_id2} not found.')
    if not report_id in corrected_counts.columns:
        return html.Div(f'No expression for {report_id}')

    gene1_counts = corrected_counts.loc[ensg_id1]
    gene2_counts = corrected_counts.loc[ensg_id2]
    log_ratio = (gene1_counts - gene2_counts).sort_values()

    title = f'{gene1}/{gene2} Expression'

    return getBlueRedLinePlot(log_ratio, title, report_id, ylabel='Gene Expression Ratio [log2]')


def create_layout(app, base_url, report_service):
    if ZSCORE_FILE not in report_service.getMergeFiles():
        print(report_service.getMergeFiles())
        return wrapInHeader(app, base_url, report_service,
            html.Div(f'File {ZSCORE_FILE} not found.'))
    zscores = pd.read_csv(
        report_service.openMergeFile(ZSCORE_FILE),
        sep='\t',
        index_col=0
    )

    if CORRECTED_COUNTS_FILE not in report_service.getMergeFiles():
        print(report_service.getMergeFiles())
        return wrapInHeader(app, base_url, report_service,
            html.Div(f'File {CORRECTED_COUNTS_FILE} not found.'))
    corrected_counts = pd.read_csv(
        report_service.openMergeFile(CORRECTED_COUNTS_FILE),
        sep='\t',
        index_col=0
    )

    return wrapInHeader(
        app,
        base_url,
        report_service,
        [
            html.Div(
                [
                    html.Div(
                        [
                            html.H6(
                                ["Expression"], className="subtitle padded"
                            ),
                        ],
                        className="twelve columns",
                    )
                ],
                className="row",
            ),

            # Row 2.
            html.Div(
                [
                    html.Div(
                        [
                            getPlotForZscore(zscores, 'BCL2', report_service.getReportId())
                        ],
                        className="six columns",
                    ),
                    html.Div(
                        [
                            getPlotForZscore(zscores, 'MCL1', report_service.getReportId())
                        ],
                        className="six columns",
                    )
                ],
                className="row",
            ),

            # Row 3.
            html.Div(
                [
                    html.Div(
                        [
                            getPlotForZscore(zscores, 'TNFRSF17', report_service.getReportId(), aka='BCMA')
                        ],
                        className="six columns",
                    ),
                    html.Div(
                        [
                            getPlotForGeneRatio(corrected_counts, 'BCL2', 'BCL2L1', zscores.Gene, report_service.getReportId())
                        ],
                        className="six columns",
                    )
                ],
                className="row",
            ),
        ],
    )

