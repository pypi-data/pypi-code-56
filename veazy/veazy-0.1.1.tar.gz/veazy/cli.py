import os
import sys
import click
import subprocess
import pydotplus
from pathlib import Path
from veazy import Veazy

@click.command()
@click.version_option()
@click.option('-r', '--root-file',
    type=click.Path(exists=True, resolve_path=True),
    help='A top-level entry from where relative depth is determined.'
)
@click.argument('src', 
    nargs=-1,
    type=click.Path(exists=True, resolve_path=True)
)
@click.option('-o', '--output-file', 'dst',
    type=click.Path(writable=True, resolve_path=True,),
    help='Write to this file. If None, svgs go to graph.svg'
)
@click.option('-c', '--complexity-offset',
    type=int, default=0, 
    help='To adjust the automatic depth. When depth is passed, this value is ignored.'
)
@click.option('-d', '--depth', type=int)
@click.option('-t', '--output-type',
              type =click.Choice(['dot', 'svg'], case_sensitive = False),
              default = 'svg',
              help='Output format. For svg, you need to have graphviz installed.'
)
def cli(src, dst, complexity_offset, depth, root_file, output_type):
    """
    Visualise your python codebase eazily.

    When ROOT_FILE is passed, the complexity may be found automatically.
    You may alter this using the --complexity-offset option, or by passing an explicit --depth.
    All nodes below the maximum depth will be summarized and their color will be gray.

    Alternatively, pass '--depth -1' to see the complete graph.
    This will include scripts/methods/functions that are not actually used.
    To cut that off, pass a ROOT_FILE and set depth to something large.


    """
    _cli(src, dst, complexity_offset, depth, root_file, output_type)

def _cli(src, dst, complexity_offset, depth, root_file, output_type):
    if len(src)==0:
        src = tuple(['.'])
    src = src + (root_file, )
    input_files, main_dir = get_all_files(src)
    root_file = root_file.split(main_dir)[1]

    cmd = ' '.join([
        f'cd "{main_dir}"; pyan3',
    	*input_files,
    	'--uses --no-defines --colored --nested-groups --annotated --dot',
	]).encode('utf-8')
    dot_lines = (
    	subprocess
    	.run(cmd, shell=True, stdout=subprocess.PIPE)
    	.stdout
    	.decode('utf-8')
	)

    pygraph = pydotplus.graphviz.graph_from_dot_data(dot_lines)

    if depth == -1:
        output = pygraph
    elif not root_file:
            no_root_msg = "Please specify a root file as '-r ROOT_FILE'"\
            + ", so we can trade off complexity. " \
            + "Alternatively, set depth=-1 and see the whole thing"
            click.echo(no_root_msg)
            sys.exit(1)
    else:
        try:
            vh = Veazy(pygraph, root_file)
        except ValueError as e:
            click.echo('The ROOT_FILE does not call any SRC code.')
            raise click.BadParameter()
        if not depth:
            depth = vh.find_auto_depth() + complexity_offset
        output = vh.prune_depth(depth)

    if output_type == 'dot':
        if not dst:
            click.echo(output.to_string())
        else:                
            with open(dst, 'w') as fo:
                fo.write(output.to_string(), '\n')
    else:
        if dst==None:
            dst = 'graph.svg'
        output.write_svg(dst)
        if dst==None:
            click.launch(f'{dst}')
        
    click.echo(f'Veazy is done after going {depth} deep. Bleeep.')
    return 0


def get_all_files(src):
    """
    src is a tuple of files and directories. 
    Directories are recursively expanded for all contained .py files. 
    When src is empty, use '.'.
    """

    if type(src) == str:
        src = tuple([src])
    dirs = [d for d in src if Path(d).is_dir()]
    nondirs = [Path(f) for f in src if not Path(f).is_dir()]
    exp_dir = [file for d in dirs for file in Path(d).rglob('*.py')] 
    files = [str(x.resolve()) for x in set(exp_dir + nondirs)]
    # first sort alphabetically
    files.sort()
    # then sort on file depth
    depth = [i.count("/") for i in files]
    files = [i for _, i in sorted(zip(depth, files))]
    files.reverse()
    # finally strip unnecessary prefixes
    prefix = os.path.commonprefix(files)
    # TODO: make non-ugly code
    prefix = '/'.join(prefix.split('/')[:-1]) + '/'
    files = [i[len(prefix):] for i in files]

    return files, prefix

if __name__ == '__main__':
	cli()
