import pandas as pd
from astropy.io import fits

def save_spectra(spectra, output_file_name, format):
    if format == '.csv':
        return save_spectra_csv(spectra, output_file_name)
    elif format == '.fits':
        return save_spectra_fits(spectra, output_file_name)
    elif format == '.xml':
        return save_spectra_xml(spectra, output_file_name)
    else:
        raise InvalidExtensionError()

def save_spectra_csv(spectra, output_file_name):
    spectra_df = pd.DataFrame.from_records([spectrum.spectrum_to_dict() for spectrum in spectra])
    spectra_df.to_csv(f'{output_file_name}.csv', index=False)
    # Assuming the sampling is the same for all spectra
    sampling_df = pd.DataFrame.from_records([spectra[0].sampling_to_dict()])
    sampling_df.to_csv(f'{output_file_name}_sampling.csv', index=False)

def save_spectra_fits(spectra, output_file_name):
    spectra_dicts = [spectrum.spectrum_to_dict() for spectrum in spectra]
    # Get the sampling
    sampling_dict = spectra[0].sampling_to_dict()
    # create a list of HDUs
    hdu_list = []
    # create a header to include the sampling
    hdr = fits.Header()
    #TODO: there must be a better way to print this
    hdr['Sampling'] = str(list(sampling_dict['pos']))
    primary_hdu = fits.PrimaryHDU(header=hdr)
    hdu_list.append(primary_hdu)
    # For each spectrum create a table
    for spectrum in spectra_dicts:
        # Split values to avoid duplicated data in the output file
        spectrum = {key:[value] for key, value in spectrum.items()}
        # Get length of flux (should be the same as length of error)
        flux_format = f"{len(spectrum['flux'][0])}E" # E: single precision floating
        # Define formats for each type according to FITS
        column_formats = {'source_id': 'K', 'xp': '2A', 'flux': flux_format, 'error': flux_format}
        # For each element of a spectrum, create a column and add the data
        column_list = []
        for key, value in spectrum.items():
            column = fits.Column(name=key, format=column_formats[key], array=value)
            column_list.append(column)
        hdu = fits.BinTableHDU.from_columns(fits.ColDefs(column_list))
        hdu_list.append(hdu)
    # Put all HDUs together
    hdul = fits.HDUList(hdu_list)
    # Write the file and replace it if it already exists
    hdul.writeto(f'{output_file_name}.fits', overwrite=True)

def to_xml(spectra, sampling, filename=None, label='spectrum', mode='w'):
    # add sampling
    sampling_str = f'<sampling>\n  <field name="pos">{sampling}</field></pos>\n</sampling>\n'
    def row_to_xml(row):
        xml = [f'<{label}>']
        # add spectra
        for i, col_name in enumerate(row.index):
            xml.append('  <field name="{0}">{1}</field>'.format(col_name, row.iloc[i]))
        xml.append(f'</{label}>')
        return '\n'.join(xml)
    result = '\n'.join(spectra.apply(row_to_xml, axis=1))
    with open(filename, mode) as f:
        f.write(sampling_str + result)

# Set custom method to pandas
pd.DataFrame.to_xml = to_xml

def save_spectra_xml(spectra, output_file_name):
    sampling = spectra[0].sampling_to_dict()['pos']
    spectra_df = pd.DataFrame.from_records([spectrum.spectrum_to_dict() for spectrum in spectra])
    spectra_df.to_xml(sampling, f'{output_file_name}.xml')
    return None
