import sys

from scruf import compare, execute, parse, run


def run_files(filenames, options):
    success = True
    for filename in filenames:
        success &= run_file(filename, options)
    return success


def run_file(filename, options):
    try:
        with open(filename, "r") as f:
            lines = f.readlines()
    except (OSError, IOError) as file_error:
        print(
            "Failed to open file {}: {}".format(filename, file_error), file=sys.stderr
        )
        return False

    parser = parse.Parser(options["indent"])
    try:
        tests = parser.parse(lines)
    except parse.ProgressionError as e:
        print("Error in parsing file {}: {}".format(filename, e), file=sys.stderr)
        return False

    try:
        executor = execute.Executor(shell=options["shell"], cleanup=options["cleanup"])
    except execute.FailedToCreateTestDirError as e:
        print("Failed to setup test environment: {}".format(e), file=sys.stderr)
        return False

    return tap_runner(tests, executor)


def tap_runner(tests, executor):
    success = True
    print("1..{}".format(len(tests)))
    for i, test in enumerate(tests):
        test_number = i + 1
        test_summary = get_test_summary(test, test_number)
        exec_result = executor.execute(test.command)

        try:
            compare_output = run.run_test(test, exec_result)
        except (compare.RegexError, execute.OutOfLinesError) as e:
            print(tap_failure(test_summary))
            print(tap_error_line(e), file=sys.stderr)
            success = False
            continue

        failed_tests = [r for r in compare_output if not r["comparison_result"]]
        if len(failed_tests) == 0:
            print(tap_success(test_summary))
        else:
            print(tap_failure(test_summary))
            for test in failed_tests:
                failure_lines = [
                    tap_comment_line("\t" + line)
                    for line in run.get_printable_failures(test)
                ]
                print("\n".join(failure_lines), file=sys.stderr)
            success = False
    return success


def tap_success(content):
    return "ok " + content


def tap_failure(content):
    return "not ok " + content


def tap_comment_line(content):
    return "# " + content


def tap_error_line(error):
    return tap_comment_line("\t" + str(error))


def get_test_summary(test, test_number):
    test_line = str(test_number)
    if test.description:
        test_line += " - {}".format(test.description.rstrip())
    return test_line
