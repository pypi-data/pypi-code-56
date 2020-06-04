import collections
import glob
import os
import re


def parse_dihedrals_directory(dihedrals_dir):
    """Parse the directory containing dihedrals xvg files.

    Args:
        dihedrals_dir (str): the dihedrals directory
    """

    xvg_files = glob.glob(os.path.join(dihedrals_dir, '*.xvg'))

    xvg_files = [re.split(r'(chi\d+)([A-Z]+)(\d+).xvg', os.path.basename(filename))
                 for filename in xvg_files]

    xvg_files.sort(key=lambda x: int(x[3]))

    xvg_files = [v[1:4] for v in xvg_files]

    xvg_contents = collections.OrderedDict()

    for chi_number, residue_name, residue_id in xvg_files:
        key = '{}{}'.format(residue_name, residue_id)
        if key in xvg_contents:
            xvg_contents[key].append(chi_number)
        else:
            xvg_contents[key] = [chi_number]

    for chis in xvg_contents.values():
        chis.sort()

    return xvg_contents


if __name__ == '__main__':

    import sys

    parse_dihedrals_directory(sys.argv[1])
