import click
import re


@click.command()
@click.option("--file", type=click.Path(exists=True))
@click.option("--tag", type=str)
@click.option("--replace", nargs=2, type=str)
def main(file, tag, replace):
    match = re.match(r"v?(?P<a>\d+)(?P<b>\.\d+)(?P<c>\.\d+)?", tag)

    version = match.expand(r"\g<a>\g<b>\g<c>")

    print(f"Pump version '{version}'")

    with open(file, "r") as f:
        content = f.read()

    content = content.replace(replace[0], replace[1].replace(r"${VERSION}", version))

    with open(file, "w") as f:
        f.write(content)


if __name__ == "__main__":
    main()
