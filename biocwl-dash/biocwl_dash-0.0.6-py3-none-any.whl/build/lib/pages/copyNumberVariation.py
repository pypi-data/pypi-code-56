import base64
import io
import glob
import os

import dash
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
from pdf2image import convert_from_bytes

from ..utils import Header, make_dash_table, wrapInHeader


def create_layout(app, base_url, report_service):
    facets_output_path = [
        f for f in report_service.getPrimaryFiles() if f.endswith("facets_output.txt")
    ]
    facets_genome_segnments_path = [
        f for f in report_service.getPrimaryFiles() if f.endswith("genome_segments.pdf")
    ]

    if not facets_output_path or not facets_genome_segnments_path:
        return wrapInHeader(
            app,
            base_url,
            report_service,
            html.H6("No facets files found.", className="subtitle padded"),
        )

    facets_output_path = facets_output_path[0]
    facets_genome_segnments_path = facets_genome_segnments_path[0]

    # We pull out all images from the PDF, and for each one keep track of:
    # - the name
    # - the image, encoded as binary data
    #     * see https://community.plot.ly/t/adding-local-image/4896/5
    genome_segnments_image_names = []
    genome_segnments_image_encodings = []

    with report_service.openPrimaryFile(facets_genome_segnments_path, "rb") as f:
        image = convert_from_bytes(f.read(), 65)[0]
    png_bytes = io.BytesIO()
    image.save(png_bytes, "png")
    png_base64 = base64.b64encode(png_bytes.getvalue())
    encoded = "data:image/png;base64,{}".format(png_base64.decode("utf-8"))

    genome_segnments_image_names.append(f"Image with ID {image.getdata().id}")
    genome_segnments_image_encodings.append(encoded)
    df_cnvs = pd.read_csv(report_service.openPrimaryFile(facets_output_path), sep="\t")

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
                                ["Copy Number Variations"], className="subtitle padded"
                            ),
                            html.P(
                                [
                                    f"This page will summarize Copy Number Variation for report ID {report_service.getReportId()}."
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
                                ["Facets Summary"],
                                className="subtitle tiny-header padded",
                            ),
                            html.Div(
                                [
                                    html.Div(
                                        [
                                            html.Div(
                                                [
                                                    html.Strong(
                                                        ["Tumor Purity"],
                                                        style={"color": "#515151"},
                                                    )
                                                ],
                                                className="three columns right-aligned",
                                            ),
                                            html.Div(
                                                [
                                                    html.P(
                                                        [float(df_cnvs["purity"])],
                                                        style={"color": "#7a7a7a"},
                                                    )
                                                ],
                                                className="nine columns",
                                            ),
                                        ],
                                        className="row",
                                        style={
                                            "background-color": "#f9f9f9",
                                            "padding-top": "20px",
                                        },
                                    ),
                                    html.Div(
                                        [
                                            html.Div(
                                                [
                                                    html.Strong(
                                                        ["Tumor Ploidy"],
                                                        style={"color": "#515151"},
                                                    )
                                                ],
                                                className="three columns right-aligned",
                                            ),
                                            html.Div(
                                                [
                                                    html.P(
                                                        [float(df_cnvs["ploidy"])],
                                                        style={"color": "#7a7a7a"},
                                                    )
                                                ],
                                                className="nine columns",
                                            ),
                                        ],
                                        className="row",
                                        style={"background-color": "#f9f9f9"},
                                    ),
                                    html.Div(
                                        [
                                            html.Div(
                                                [
                                                    html.Strong(
                                                        ["digLogR"],
                                                        style={"color": "#515151"},
                                                    )
                                                ],
                                                className="three columns right-aligned",
                                            ),
                                            html.Div(
                                                [
                                                    html.P(
                                                        [float(df_cnvs["digLogR"])],
                                                        style={"color": "#7a7a7a"},
                                                    )
                                                ],
                                                className="nine columns",
                                            ),
                                        ],
                                        className="row",
                                        style={"background-color": "#f9f9f9"},
                                    ),
                                ],
                                className="fees",
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
                            html.H6(
                                ["Copy Number Variation Visualization"],
                                className="subtitle tiny-header padded",
                            )
                        ],
                        className="twelve columns",
                    )
                ],
                className="row ",
            ),
            # Row 4
            html.Div(
                [
                    html.Img(
                        src=genome_segnments_image_encodings[0],
                        style={
                            "height": "100%",
                            "width": "100%",
                            "overflow": "visible",
                        },
                    )
                ],
                style={"overflow": "visible", "textAlign": "center"},
            ),
        ],
    )

