#!/usr/bin/env python
from __future__ import print_function
import logging
from collections import OrderedDict

from multiqc.plots import table
from multiqc.modules.base_module import BaseMultiqcModule

from .bbmap_filetypes import file_types, section_order

""" MultiQC module to parse output from BBMap """

# Initialize the logger
log = logging.getLogger(__name__)

class MultiqcModule(BaseMultiqcModule):
    """ BBMap module, tries to identify and parse tons of output files
    generated by BBMap.
    """

    def __init__(self):
        super(MultiqcModule, self).__init__(
            name="BBTools",
            anchor="bbmap",
            href="http://jgi.doe.gov/data-and-tools/bbtools/",
            info="""is a suite of fast multithreaded bioinformatics tools
            designed for the analysis of DNA and RNA sequence data."""
        )

        # Init data dict
        self.mod_data = { key:{} for key in file_types }

        # Find output files
        module_filetypes = [('bbmap/'+ft, ft) for ft in file_types]
        data_found = False
        for module_filetype, file_type in module_filetypes:
            for f in self.find_log_files(module_filetype, filehandles=True):
                if self.parse_logs(file_type, **f):
                    self.add_data_source(f)
                    data_found = True

        if not data_found:
            raise UserWarning
        else:
            num_samples = max([len(self.mod_data[ft].keys()) for ft in self.mod_data])
            log.info("Found {} reports".format(num_samples))

        for file_type in section_order:
            if len(self.mod_data[file_type]) > 0:
                log.debug("section %s has %d entries", file_type,
                          len(self.mod_data[file_type]))

                if file_types[file_type]['plot_func']:
                    self.add_section(
                        name = file_types[file_type]['title'],
                        anchor =  'bbmap-' + file_type,
                        description = file_types[file_type]['descr'],
                        helptext = file_types[file_type]['help_text'],
                        plot = self.plot(file_type)
                    )

            if any(self.mod_data[file_type][sample]['kv']
                   for sample in self.mod_data[file_type]):
                self.add_section(
                    name = file_types[file_type]['title']+' summary table',
                    anchor =  'bbmap-' + file_type + '-table',
                    description = file_types[file_type]['descr'],
                    helptext = file_types[file_type]['help_text'],
                    plot = self.make_basic_table(file_type)
                )


    def parse_logs(self, file_type, root, s_name, fn, f, **kw):

        if self.is_ignore_sample(s_name):
            return False

        log.debug("Parsing %s/%s", root, fn)
        if not file_type in file_types:
            log.error("Unknown output type '%s'. Error in config?", file_type)
            return False
        log_descr = file_types[file_type]
        if 'not_implemented' in log_descr:
            log.debug("Can't parse '%s' -- implementation missing", file_type)
            return False

        cols = log_descr['cols']
        if isinstance(cols, OrderedDict):
            cols = list(cols.keys())

        kv = {}
        data = {}
        for line_number, line in enumerate(f, start=1):
            line = line.strip().split('\t')
            try:
                header_row = line[0][0] == '#'
            except IndexError:
                continue  # The table is probably empty
            if header_row:
                line[0] = line[0][1:] # remove leading '#'

                if line[0] != cols[0]:
                    # It's not the table header, it must be a key-value row
                    if len(line) == 3 and file_type == "stats":
                        # This is a special case for the 'stats' file type:
                        # The first line _might_ have three columns if processing paired-end reads,
                        # but we don't care about the first line.
                        # The third line is always three columns, which is what we really want.
                        if line[0] == "File":
                            continue
                        kv["Percent filtered"] = float(line[2].strip("%"))
                        kv[line[0]] = line[1]
                    elif len(line) != 2:
                        # Not two items? Wrong!
                        log.error("Expected key value pair in %s/%s:%d but found '%s'",
                                  root, s_name, line_number, repr(line))
                        log.error("Table header should begin with '%s'",
                                  cols[0])
                    else:
                        # save key value pair
                        kv[line[0]] = line[1]
                else:
                    # It should be the table header. Verify:
                    if line != cols:
                        if line != cols + list(log_descr['extracols'].keys()):
                            log.error("Table headers do not match those 'on file'. %s != %s",
                                      repr(line), repr(cols))
                        return False
            else:
                if isinstance(log_descr['cols'], OrderedDict):
                    line = [
                        value_type(value)
                        for value_type, value in zip(log_descr['cols'].values(), line)
                    ]
                else:
                    line = list(map(int, line))
                data[line[0]] = line[1:]

        if not data:
            log.warning("File %s appears to contain no data for plotting, ignoring...", fn)
            return False

        if s_name in self.mod_data[file_type]:
            log.debug("Duplicate sample name found! Overwriting: %s", s_name)

        self.mod_data[file_type][s_name] = {'data':data, 'kv': kv}
        log.debug("Found %s output for sample %s with %d rows",
                  file_type, s_name, len(data))

        return True

    def plot(self, file_type):
        """ Call file_type plotting function.
        """

        samples = self.mod_data[file_type]
        plot_title = file_types[file_type]['title']
        plot_func = file_types[file_type]['plot_func']
        plot_params = file_types[file_type]['plot_params']
        return plot_func(samples,
                    file_type,
                    plot_title=plot_title,
                    plot_params=plot_params)


    def make_basic_table(self, file_type):
        """  Create table of key-value items in 'file_type'.
        """

        table_data = {sample: items['kv']
                for sample, items
                in self.mod_data[file_type].items()
        }
        table_headers = {}
        for column_header, (description, header_options) in file_types[file_type]['kv_descriptions'].items():
            table_headers[column_header] = {
                    'rid': '{}_{}_bbmstheader'.format(file_type, column_header),
                    'title': column_header,
                    'description': description,
            }
            table_headers[column_header].update(header_options)

        tconfig = {
            'id': file_type + '_bbm_table',
            'namespace': 'BBTools'
        }
        for sample in table_data:
            for key, value in table_data[sample].items():
                try:
                    table_data[sample][key] = float(value)
                except ValueError:
                    pass
        return table.plot(table_data, table_headers, tconfig)
