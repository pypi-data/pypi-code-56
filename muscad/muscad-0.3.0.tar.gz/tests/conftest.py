import os


def compare(part, scad_file):
    filepath = os.path.join(
        os.path.dirname(__file__), "target_scad_files", scad_file
    )
    with open(filepath, "rt") as finput:
        scad = "".join(finput.readlines())
    render = part.render()
    assert render == scad
