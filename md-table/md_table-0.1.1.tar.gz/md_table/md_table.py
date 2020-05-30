import click
import csv


def get_type_of_line(alignment: str):
    if alignment == "right":
        return "-:"
    if alignment == "center":
        return ":-:"
    if alignment == "left":
        return ":-"
    return "-"


def create_md_table(rows: list, alignment="left"):
    row_strs = []
    max_row_len = 0
    for row in rows:
        if not all(isinstance(ele, str) for ele in row):
            row = map(str, row)
        if max_row_len < len(row):
            max_row_len = len(row)
        row_str = "|" + "|".join(row) + "|"
        row_strs.append(row_str)
    table = ""
    table = row_strs.pop(0)
    table += "".join(["|"] * (max_row_len + 1 - table.count("|")))
    table += "\n|" + "|".join(([get_type_of_line(alignment.lower())] * max_row_len)) + "|\n" + "\n".join(row_strs)
    return table


@click.command()
@click.option('--input', "-i", "input", type=click.Path(exists=True), help='csv file to read')
@click.option('--file_delimiter', "-fd", "fd", default=",", help='csv file delimiter')
@click.option('--text_alignment', "-ta", "text_alignment", default="left",
              help='alignment of the table text possible values, "left", "right" and "center".'
                   'This is case insensitive.')
@click.option('--output', "-o", "output", help='write markdown table to file')
@click.option('--output_mode', "-om", "output_mode", default="a+", help='output write mode')
def main(input, fd, text_alignment, output, output_mode):
    with open(input, "r") as f:
        reader = csv.reader(f, delimiter=fd)
        rows = [row for row in reader]
        md_table = create_md_table(rows, text_alignment)
        if output:
            with open(output, output_mode) as output_file:
                output_file.write(md_table)
                print("successfully written to", output, "in", output_mode, "mode")
        else:
            print(md_table)


if __name__ == '__main__':
    main()
