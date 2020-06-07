#!/usr/bin/env python3
"""Command-line interface for the tool."""

import argparse

import os.path
from writerblocks.common import (CONFIG_FILENAME, DEFAULT_OPTIONS, FORMAT_FILENAME,
                                 DEFAULT_FMT, options)
from writerblocks.backend import (get_index_file_path, combine_from_index,
                                  read_org_file, write_contents_to_file,
                                  preamble_to_tex, new_project, full_path)


from typing import Optional, List


def setup_parser():
    parser = argparse.ArgumentParser(
        description="A toolkit for writing stories in a modular way.")

    parser.add_argument('-d', '--base-dir', type=os.path.abspath,
                        help="Directory in which project files are stored; if "
                             "not specified, current directory will be used")
    parser.add_argument('-f', '--out-fmt',
                        help="File format to export projects to (default: {})"
                        .format(DEFAULT_OPTIONS.out_fmt))
    parser.add_argument('-r', '--in-fmt', help="Text file format (default: {})"
                        .format(DEFAULT_OPTIONS.in_fmt))
    parser.add_argument('-o', '--out-file',
                        help='Output file name, not including extension'
                             ' (default: "{}")'.format(DEFAULT_OPTIONS.out_file))
    parser.add_argument('-i', '--index-file',
                        help='Index file to use; if not provided, will attempt '
                             'to automatically locate in project directory')
    parser.add_argument('-t', '--tags', nargs='+',
                        help="Ignore text files that don't have these tags "
                             "(space-separated)")
    parser.add_argument('-a', '--all-tags', action='store_true',
                        help='Use only files that match *all* specified tags'
                             ' (overrides default behavior)')
    parser.add_argument('-b', '--blacklist-tags', nargs='+',
                        help='Ignore files with these tags (space-separated)')
    parser.add_argument('-n', '--new-project', action='store_true',
                        help='Create a new project with default contents.')

    parser.epilog = ("""All other command-line options will be passed to pandoc 
                     when output is generated.\n
                     All options except --all-tags, --base-dir and --new-project
                     may be set in config.yaml; command-line options will override 
                     config file ones.""")
    return parser


def parse_options(user_args: argparse.Namespace,
                  pandoc_args: Optional[List[str]]) -> argparse.Namespace:
    """Collect and organize the various options set by the user.

    Priority: user-specified options override config-file options, which
    in turn override the default options.
    """
    if pandoc_args:
        user_args.pandoc_args = pandoc_args
    # Need to identify base directory to find config files.
    if user_args.base_dir:
        options.base_dir = user_args.base_dir
    config_filename = full_path(CONFIG_FILENAME)
    fmt_filename = full_path(FORMAT_FILENAME)
    options.fmt = read_org_file(fmt_filename) if os.path.exists(fmt_filename) else DEFAULT_FMT
    config = read_org_file(config_filename) if os.path.exists(config_filename) else {}
    # Only try to find index file if we expect it to exist.
    if user_args.index_file and not user_args.new_project:
        options.index_file = get_index_file_path(filename=user_args.index_file)

    # Convert to dicts for ease of combining.
    user_opts = vars(user_args)
    base_opts = vars(options)
    # Replace default options with config file options first.
    for opt in config:
        base_opts[opt] = config[opt]
    # Replace with command-line options next.
    for opt in user_opts:
        if user_opts[opt] is not None:
            base_opts[opt] = user_opts[opt]
    # Finally, if there's a specified "preamble" file be sure we include it.
    if options.fmt.get('preamble'):
        preamble = preamble_to_tex()
        options.pandoc_args.append('--include-before-body={}'.format(preamble))
    return options


def main():
    """Run the command-line writerblocks tool."""
    parser = setup_parser()
    opts = parse_options(*parser.parse_known_args())
    if opts.new_project:
        new_project()
        return "Created project files in {}".format(opts.base_dir)
    try:
        text = combine_from_index(index_filename=opts.index_file, tags=opts.tags,
                                  blacklist_tags=opts.blacklist_tags,
                                  match_all=opts.all_tags,
                                  include_tags=False)
        write_contents_to_file(text=text)
        return "Successfully created {}".format(opts.out_file)
    except FileNotFoundError:
        # Probably there's no index file, die gracefully.
        parser.print_help()


if __name__ == '__main__':
    main()
