import click
from .explorer import get_path_all_files
from .photoSorter import PhotoSorter
from .duplicateDetector import DuplicateDetector


@click.group()
def cli():
    pass


@click.command(help="Sort recursively SRC, using metadata to create a tree "
               "like folder OUTPUT-DIR/year/month/")
@click.argument("input_dir", type=click.Path(exists=True,
                                             writable=True,
                                             file_okay=False))
@click.argument("output_dir", type=click.Path(writable=True,
                                              file_okay=False))
def sort(input_dir, output_dir):
    click.echo(f"Scanning {input_dir}")
    files_in_dest = get_path_all_files(input_dir)
    click.echo(f"Starting to tidy {input_dir} in dir {output_dir}")
    PhotoSorter(files_in_dest, output_dir)
    click.echo("Done")


@click.command(help="Compares INPUT-DIR to TARGET and detects duplicates. "
               "Moves the duplicate file in /SRC/DUPLICATES")
@click.argument("input_dir", type=click.Path(exists=True,
                                             writable=True,
                                             file_okay=False))
@click.argument("target", type=click.Path(exists=True,
                                          file_okay=False))
def compare(input_dir, target):
    if input_dir == target:
        click.echo(click.style("Same src and target. Aborting.", fg="red"))
        return
    click.echo(click.style(f"Scanning {input_dir}", fg="cyan"))
    files_in_src = get_path_all_files(input_dir)
    click.echo("\n")

    click.echo(click.style(f"Scanning {input_dir}", fg="cyan"))
    files_in_target = get_path_all_files(target)
    click.echo("\n")

    click.echo("Moving the duplicated files...")

    detector = DuplicateDetector(files_in_src, files_in_target, input_dir)
    detector.compare()

    click.echo(click.style(
        f"Moved duplicate files in {detector.path_duplicates}", fg="green"))


cli.add_command(sort)
cli.add_command(compare)
cli()
