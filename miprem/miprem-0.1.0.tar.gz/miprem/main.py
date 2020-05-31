import argparse
import os.path as op

from miprem.merit_profile import MeritProfile
import sys
import subprocess
import tempfile


def cli() -> None:
    formatter = lambda prog: argparse.HelpFormatter(prog, max_help_position=42)

    # TODO: allow stdin / stdout for file paths with '-' syntax
    parser = argparse.ArgumentParser(formatter_class=formatter, description='A tool to render Merit Profile data.')
    parser.add_argument('input_data', help='MP data input path')
    parser.add_argument('-t', '--table', action='store_true', help='Print MP data table')
    parser.add_argument('-p', '--png', help='Export to png instead svg', action='store_true')
    parser.add_argument('-o', '--output', help='MP image output path')
    parser.add_argument('-d', '--dimensions', help='Output image dimensions, as `<w>x<h>` (400x300)', metavar='DIM',
                        default='400x300')
    parser.add_argument('-s', '--sidebar_width', help='Sidebar width in %% (5)', metavar='WIDTH', default=5, type=int)
    parser.add_argument('-c', '--css_file', help='Custom CSS file to add')
    parser.add_argument('-C', '--inline_css', help='Custom inline CSS to add', default='')
    # bad_mention_color: '#FF0000'
    # medium_mention_color: '#FFFF00'
    # good_mention_color: '#00FF00'

    args = parser.parse_args()

    if not op.isfile(args.input_data):
        print('File %s can not be found.' % args.input_data)
        exit(1)

    with open(args.input_data) as input_data_file:
        mp = MeritProfile(input_data_file)

    if args.table:
        print(mp.term_table())
        exit(0)

    try:
        width, height = [int(dim) for dim in args.dimensions.split('x')]
    except ValueError:
        print('dimensions must in the form `<width>x<height>` - example: `400x300`')
        return

    user_css = ''
    if args.css_file:
        try:
            with open(args.css_file, 'w') as css_file:
                user_css += css_file.read()
        except FileNotFoundError as e:
            print(e)
            return
    if args.inline_css:
        user_css += args.inline_css

    if args.png:
        output = mp.build_png(width, height, args.sidebar_width, user_css)
    else:
        output = mp.build_svg(width, height, args.sidebar_width, user_css)

    if args.output:
        try:
            with open(args.output, 'wb') as output_file:
                output_file.write(output)
        except FileNotFoundError as e:
            print(e)
            return
    else:
        program = {'linux': 'xdg-open', 'win32': 'explorer', 'darwin': 'open'}
        with tempfile.NamedTemporaryFile() as temp_file:
            temp_file.write(mp.build_png(width, height, args.sidebar_width, user_css))
            subprocess.run([program[sys.platform], temp_file.name])


if __name__ == '__main__':
    cli()
