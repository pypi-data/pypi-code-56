#!/usr/bin/env python3
import subprocess

def subprocess_cmd(bash_cmd):
    print(bash_cmd)
    proc = subprocess.Popen(bash_cmd, stdout=subprocess.PIPE, shell=True)
    #proc = subprocess.Popen(bash_cmd, stdout=subprocess.PIPE, stderr=devnull, shell=True)
    (output, err) = proc.communicate()

    err_lines = ''
    if err != None and len(err) > 1:
        err_lines = str(err, 'utf-8').split('\n')
        if (len(err_lines) > 1):
            print(err_lines)

    out_lines = str(output, 'utf-8').split('\n')
    #out_lines = str(output).split('\n')

    """
    if (len(out_lines) > 1):
        print(out_lines)
    """

    return out_lines, err_lines

if __name__ == "__main__":
    out_lines, err_lines = subprocess_cmd('date')
    for line in out_lines:
        print(line)
    for line in err_lines:
        print("error " + line)

    out_lines, err_lines = subprocess_cmd('date2')
    for line in out_lines:
        print(line)
    for line in err_lines:
        print("error " + line)
