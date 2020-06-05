import numpy as np
import pandas as pd
from astropy.io import fits
from astropy.table import Table

def save_photometry(photometry, output_file_name, format):
    if format == '.csv':
        return save_photometry_csv(photometry, output_file_name)
    elif format == '.fits':
        return save_photometry_fits(photometry, output_file_name)
    elif format == '.xml':
        return save_photometry_xml(photometry, output_file_name)
    else:
        raise InvalidExtensionError()

def save_photometry_csv(photometry, output_file_name):
    photometry_df = pd.DataFrame.from_records([phot.photometry_to_dict() for phot in photometry])
    photometry_df.to_csv(f'{output_file_name}.csv', index=False)

def save_photometry_fits(photometry, output_file_name):
    photometry_df = pd.DataFrame.from_records([phot.photometry_to_dict() for phot in photometry])
    table = Table.from_pandas(photometry_df)
    table.write(f'{output_file_name}.fits', format='fits', overwrite=True)

def to_xml(photometry, filename=None, label='photometry', mode='w'):
    def row_to_xml(row):
        xml = [f'<{label}>']
        # add photometry
        for i, col_name in enumerate(row.index):
            xml.append('  <field name="{0}">{1}</field>'.format(col_name, row.iloc[i]))
        xml.append(f'</{label}>')
        return '\n'.join(xml)
    result = '\n'.join(photometry.apply(row_to_xml, axis=1))
    with open(filename, mode) as f:
        f.write(result)

# Set custom method to pandas
pd.DataFrame.to_xml = to_xml

def save_photometry_xml(photometry, output_file_name):
    photometry_df = pd.DataFrame.from_records([phot.photometry_to_dict() for phot in photometry])
    photometry_df.to_xml(f'{output_file_name}.xml')
    return None
