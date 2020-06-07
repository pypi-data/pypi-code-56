from subprocess import run, PIPE


def get_cmd(*args):
    output = run(args, check=True, stdout=PIPE, universal_newlines=True).stdout
    if output.endswith("\n"):
        output = output[:-1]
    return output


def run_cmd(*args):
    print("+", " ".join(args))
    run(args, check=True)
