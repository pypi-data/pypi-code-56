import base64
import io
import glob
import os

import dash
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
from pdf2image import convert_from_bytes

from ..utils import make_dash_table, wrapInHeader


# Sometimes the PDF has hundreds of images and takes a long time to load.
# Only load in the first bunch.
MAX_IMAGES = 20


def create_layout(app, base_url, report_service):
    pdf_paths = [f for f in report_service.getPrimaryFiles() if f.endswith('fusions.pdf')]
    fusion_paths = [f for f in report_service.getPrimaryFiles() if f.endswith('fusions.tsv')]

    if not pdf_paths or not fusion_paths:
        return wrapInHeader(
            app,
            base_url,
            report_service,
            html.H6(
                "No fusion files found.", className="subtitle padded"
            )
        )

    pdf_path = pdf_paths[0]
    fusions_path = fusion_paths[0]

    # We pull out all images from the PDF, and for each one keep track of:
    # - the name
    # - the image, encoded as binary data
    #     * see https://community.plot.ly/t/adding-local-image/4896/5
    fusion_image_names = []
    fusion_image_encodings = []

    with report_service.openPrimaryFile(pdf_path, 'rb') as f:
        images = convert_from_bytes(f.read(), 65)
    num_images = len(images)
    for image in images[:min(MAX_IMAGES, len(images))]:
        png_bytes = io.BytesIO()
        image.save(png_bytes, 'png')
        png_base64 = base64.b64encode(png_bytes.getvalue())
        encoded = 'data:image/png;base64,{}'.format(png_base64.decode('utf-8'))

        fusion_image_names.append(f'Image with ID {image.getdata().id}')
        fusion_image_encodings.append(encoded)

    df_fusions = pd.read_csv(
        report_service.openPrimaryFile(fusions_path),
        sep="\t")

    return wrapInHeader(app, base_url, report_service,
        [
            html.Div(
                [
                    html.Div(
                        [
                            html.H6(
                                ["Gene Fusions"], className="subtitle padded"
                            ),
                            html.P(
                                [
                                    f"This page will summarize Gene Fusions for report ID {report_service.getReportId()}."
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
                                ["Gene Fusions Table (Arriba)"],
                                className="subtitle tiny-header padded",
                            ),
                            html.Div(
                                [
                                    html.Table(
                                        make_dash_table(df_fusions),
                                        className="tiny-header",
                                    )
                                ],
                                style={"overflow-x": "auto"},
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
                                [
                                    "Gene Fusions Visualization ",
                                    f'(rendering {len(fusion_image_encodings)}/{num_images} images in PDF)'
                                ],
                                className="subtitle tiny-header padded",
                            )
                        ],
                        className="twelve columns",
                    )
                ],
                className="row ",
            ),
            # Row 4
            html.Div([
                dcc.Dropdown(
                    id='gene-fusions-image-dropdown',
                    options=[
                        {'label': label, 'value': value}
                        for label, value
                        in zip(fusion_image_names, fusion_image_encodings)],
                    value=fusion_image_encodings[0]
                ),
                html.Img(id='gene-fusions-image')
            ]),
        ])
