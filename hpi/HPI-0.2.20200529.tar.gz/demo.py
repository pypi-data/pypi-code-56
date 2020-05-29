#!/usr/bin/env python3
from subprocess import check_call, DEVNULL
from shutil import copy, copytree
import os
from os.path import abspath
from pathlib import Path

my_repo = Path(__file__).absolute().parent


def run():
    # uses fixed paths; worth it for the sake of demonstration
    # assumes we're in /tmp/my_demo now

    # 1. clone git@github.com:karlicoss/my.git
    copytree(my_repo, 'my_repo', symlinks=True)

    # 2. prepare repositories you'd be using. For this demo we only set up Hypothesis
    hypothesis_repo = abspath('hypothesis_repo')
    check_call(['git', 'clone', 'https://github.com/karlicoss/hypexport.git', hypothesis_repo])
    #

    # 3. prepare some demo Hypothesis data
    hypothesis_backups = abspath('backups/hypothesis')
    Path(hypothesis_backups).mkdir(exist_ok=True, parents=True)
    check_call([
        'curl',
        'https://raw.githubusercontent.com/taniki/netrights-dashboard-mockup/master/_data/annotations.json',
        '-o', hypothesis_backups + '/annotations.json',
    ], stderr=DEVNULL)
    #

    # 4. point my.config to the Hypothesis data
    mycfg_root = abspath('my_repo/doc/example_config')
    init_file = Path(mycfg_root) / 'my/config/__init__.py'
    init_file.write_text(init_file.read_text().replace(
        '/path/to/hypothesis/data',
        hypothesis_backups,
    ))
    #

    # 4. now we can use it!
    os.chdir(my_repo)

    check_call(['python3', '-c', '''
import my.hypothesis

pages = my.hypothesis.get_pages()

from itertools import islice
for page in islice(pages, 0, 8):
    print('URL:   ' + page.url)
    print('Title: ' + page.title)
    print('{} annotations'.format(len(page.highlights)))
    print()
'''], env={
    # this is just to prevent demo.py from using real data
    # normally, it will rely on having my.config in ~/.config/my
    'MY_CONFIG': mycfg_root,
    **os.environ,
})

# that should result in something like this:

# URL:   https://tacticaltech.org/
# Title: Tactical Technology Collective
# 1 annotations
#
# URL:   https://web.hypothes.is/blog/annotating-the-wild-west-of-information-flow/
# Title: Annotating the wild west of information flow – Hypothesis
# 1 annotations
#
# URL:   http://www.liberation.fr/futurs/2016/12/12/megafichier-beauvau-prie-de-revoir-sa-copie_1534720
# Title: «Mégafichier» : Beauvau prié de revoir sa copie
# 3 annotations
#
# URL:   https://www.wired.com/2016/12/7500-faceless-coders-paid-bitcoin-built-hedge-funds-brain/
# Title: 7,500 Faceless Coders Paid in Bitcoin Built a Hedge Fund’s Brain
# 4 annotations
#
# URL:   http://realscreen.com/2016/12/06/project-x-tough-among-sundance-17-doc-shorts/
# Title: “Project X,” “Tough” among Sundance ’17 doc shorts
# 1 annotations
#
# URL:   https://grehack.fr/2016/program
# Title: GreHack | Security conference and hacking game 2016 | Grenoble
# 1 annotations
#
# URL:   https://respectmynet.eu/
# Title: [!] Respect My Net
# 1 annotations
#
# URL:   https://www.youtube.com/watch?v=Xgp7BIBtPhk
# Title: BBC Documentaries 2016: The Joy of Data [FULL BBC SCIENCE DOCUMENTARY]
# 1 annotations

from contextlib import contextmanager
@contextmanager
def named_temp_dir(name: str):
    """
    Fixed name tmp dir
    """
    td = (Path('/tmp') / name)
    try:
        td.mkdir(exist_ok=False)
        yield td
    finally:
        import shutil
        shutil.rmtree(str(td))


def main():
    with named_temp_dir('my_demo') as tdir:
        os.chdir(tdir)
        run()


if __name__ == '__main__':
    main()
