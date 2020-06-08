import os
import glob
import re


def files_to_inputs(file_list):
    from ccjob import Input
    """ Create multiple Input objects based on file list.

    Parameters
    ----------
    file_list : list
        List of input filenames (assumes to be in working directoy).

    Returns
    -------
    : list
        List of ccjob.Input objects.
    """
    # sanity check
    if not all([os.path.isfile(f) for f in file_list]):
        raise FileExistsError('File in list does not exist!')

    return [Input.from_file(f) for f in file_list]

def get_all_inputs(extension='in', wdir=os.getcwd()):
    """ Turn all input filenames in folder into Input objects.

    Parameters
    ----------
    extension : str
        File extension for input files (default: 'in').
    wdir : str
        Working directory path (default: current directory).

    Returns
    -------
    inputs : list
        List of ccjob.Input objects.
    """

    files  = [x for x in os.listdir(wdir) if os.path.isfile(x) and \
              os.path.splitext(x)[1][1:] == extension]
    inputs = files_to_inputs(files)
    return inputs

def submit_all_inputs(options, extension='in', wdir=os.getcwd(), dry_run=True):
    """ Submit all input files in folder at once.

    Parameters
    ----------
    options : dict
        Dictionary of job parameters (see ccjob.Job class).
        [Caution] The same set of options is used for all jobs!
    extension : str
        Input file extension (default: 'in').
    wdir : str
        Submit directory (default: current working directory).
    dry_run : bool
        Only print submission command without actually submitting job.
    """
    from ccjob import Job
    inputs = get_all_inputs(extension=extension, wdir=wdir)

    # sanity check for minimum requirements
    min_req = ['script']
    if not all([m in options for m in min_req]):
        raise KeyError('Minimum requirements for options not met!')

    # create list of jobs and print configuration
    jobs = [Job(i, **options) for i in inputs]
    for job in jobs:
        job.submit(dry_run=True)

    # ask user to confirm
    print('-'*80)
    print("[!] You're about to submit jobs in the configuration defined above.")
    final_ok = input("Continue? [y/n]: ")
    if final_ok.lower() in ['y', 'yes']:
        for job in jobs:
            job.submit(dry_run=dry_run)
    else:
        print("Aborted.")

def find_output(directory, extension="out", abspath=True):
    """ Find output file in a directory.

    Parameters
    ----------
    directory : str
        Path to folder in which output should be located.
    extension : str
        File extension of output file (default: 'out').
    abspath : bool
        Whether to return absolute path (default: True).

    Returns
    -------
    outpath : str
        Path to output file (relative or absolute, default: absolute).
    """
    dir_list = [fn for fn in glob.glob(directory+"/*."+extension)
                if not os.path.basename(fn).startswith("slurm")]

    if len(dir_list) != 1:
        err = f"Could not determine unique .{extension} file in {directory}/ !"
        raise FileNotFoundError(err)
    else:
        outpath = dir_list[0]
        if abspath:
            outpath = os.path.abspath(dir_list[0])
        return outpath

def find_eleconfig(directory, abspath=True):
    """Find a suitable electronic configuration file in a directory.

    Parameters
    ----------
    directory : str
        Search directory for finding electronic configuration file.
    abspath : bool
        Whether to return absolute path (default: True).

    Returns
    ----------
    elconf_path : str or int
         Path to 'eleconfig.txt'.
    """
    usual_suspects = ["eleconfiguration.txt", "eleconfig.txt",
                      "elconfig.txt", "eleconf.txt", "econf.txt",
                      "elconf.txt", "ele.config", "electronic.conf",
                      "ccjob_elconfig.txt"
                     ]
    cand = [os.path.basename(fn) for fn in glob.glob(directory+"/*.txt")
            if os.path.isfile(fn)]
    cand.extend([os.path.basename(cf) for cf in glob.glob(directory+"/*.config")
                 if os.path.isfile(cf)])

    intersec = [x for x in cand if x.lower() in usual_suspects]
    if len(intersec) != 1:
        err = "No or more than one electronic configuration file detected!"
        raise FileNotFoundError(err)
    else:
        elconf_path = intersec[0]
        if abspath:
            elconf_path = os.path.abspath(elconf_path)
            #absdir  = os.path.abspath(directory)
            #outpath = os.path.join(absdir, intersec[0])
        return elconf_path

def module_exists(module_name):
    """ Check if a module can be imported. """
    try:
        __import__(module_name)
    except ImportError:
        return False
    else:
        return True

def split_path(filepath):
    """
    Make absolute path and split filename from path.
    """
    dirname  = os.path.dirname(filepath)
    filename = os.path.basename(filepath)
    if len(dirname) == 0:
        # filepath is just a filename
        # set dirname to current working dir
        absdir = os.getcwd()
    else:
        absdir = os.path.abspath(dirname)
    return absdir, filename

# TODO: remove dependency on q-chem format (ghost)
def zr_frag(fname, separator="----", fmt="string"):
    """ Get fragment coordinates from .zr file

    Parameters
    ----------
    fname: string
        ZR filename
    separator: string
        Separator.
    fmt: string
        Format specifier. Possible options: "list", "string"

    Returns
    -------
    frags: dict
        Dictionary of list of lists with fragment coordinates and atom symbol,
        e.g. ``frags["A"] = ["C 0.0 0.1 0.0", "..."]``. If no separator is
        found (normal xyz file), only one fragment is assumed ("AB").

        If fragments are found ``frags`` will contain the keys 'A', 'B', 'AB',
        'AB_ghost'.


    """
    if fmt.lower() not in ("string", "list"):
        raise ValueError("Invalid format option specified! Use either 'string' or 'list'.")
    with open(fname) as zr:
        rl = zr.readlines()
    line_B = 0
    frags = {}
    for i, line in enumerate(rl):
        if separator in line:
            line_B = i

    if line_B == 0:
        frags["AB"] = list(map(str.split, rl[0:]))
    else:
        frags["A"] = list(map(str.split, rl[0:line_B]))
        frags["B"] = list(map(str.split, rl[line_B+1:]))
        frags["AB_ghost"] = frags["A"] + list(map(lambda x: ["@"+x[0]]+x[1:],
                                                  frags["B"]))
        frags["BA_ghost"] = list(map(lambda x: ["@"+x[0]]+x[1:], frags["A"]))+\
                            frags["B"]
        frags["AB"] = frags["A"] + frags["B"]

    if fmt=="list":
        return frags
    elif fmt=="string":
        for key in frags:
            frags[key] = "\n".join(["    ".join(s) for s in frags[key]])
        return frags


# TODO: generalize for N fragments
def read_eleconfig(fname="eleconfig.txt", silent=False):
    """Read electronic configuration from file.

    Format:
      `charge_tot = 0`
      `multiplicity_tot = 1`

    Parameters
    ----------
    fname : str
        Input file name (default: 'eleconfig.txt').
    silent : bool
        Whether to print information to screen or not.

    Returns
    -------
    eleconfig : dict
        Dictionary containing the electronic configuration. If no file was
        found, an empty dictionary will be returned instead.
    """
    p_chg = r"charge_(?P<frag>[A-Za-z0-9]+)\s*=\s*(?P<value>[-+]?\d+)"
    p_mul = r"multiplicity_(?P<frag>[A-Za-z0-9]+)\s*=\s*(?P<value>\d+)"
    eleconfig = {}
    if os.path.exists(fname):
        with open(fname) as el:
            for x in el:
                m = re.search(p_chg, x)
                if m:
                    if m.group("frag") == "tot":
                        eleconfig["charge_tot"] = int(m.group("value"))
                    elif m.group("frag") in ["A", "a", "1"]:
                        eleconfig["charge_a"]   = int(m.group("value"))
                    elif m.group("frag") in ["B", "b", "2"]:
                        eleconfig["charge_b"]   = int(m.group("value"))
                m = re.search(p_mul, x)
                if m:
                    if m.group("frag") == "tot":
                        eleconfig["multiplicity_tot"] = int(m.group("value"))
                    elif m.group("frag") in ["A", "a", "1"]:
                        eleconfig["multiplicity_a"]   = int(m.group("value"))
                    elif m.group("frag") in ["B", "b", "2"]:
                        eleconfig["multiplicity_b"]   = int(m.group("value"))
        print(f"-- Obtained electronic configuration from file '{fname}'.")
    else:
        print(("Could not find electronic configuration file. Using default "
               "values for charge and multiplicity (c=0, m=1)."))
    return eleconfig

def eleconfig_update(*dct, fname="eleconfig.txt"):
    """Update dictionary with charge and multiplicity from file.

    """
    eleconfig = read_eleconfig(fname)
    if len(dct) == 1:
        dct[0].update(eleconfig)
    else:
        return eleconfig
