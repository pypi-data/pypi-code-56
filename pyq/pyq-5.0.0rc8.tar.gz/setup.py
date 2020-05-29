"""PyQ - Python for kdb+

PyQ brings the Python programming language to the kdb+ database.  It allows
developers to seamlessly integrate Python and q codes in one application.
This is achieved by bringing the Python and q interpreters in the same
process so that codes written in either of the languages operate on the same
data.  In PyQ, Python and q objects live in the same memory space and share
the same data.

"""
import os
import platform
import subprocess
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from distutils.core import Command, Distribution, Extension
from distutils.command.build import build
from distutils.command.build_ext import build_ext
from distutils.command.config import config
from distutils.command.install import install
from distutils.command.install_data import install_data
from distutils.command.install_scripts import install_scripts

import sysconfig

WINDOWS = platform.system() == 'Windows'
VERSION_FILE = 'src/pyq/version.py'
CFLAGS = ['/WX', '/wd4090'] if WINDOWS else ['-fno-strict-aliasing']

if sys.version_info >= (3, ) and not WINDOWS:
    CFLAGS.append('-Werror')

LDFLAGS = []
if (sys.maxsize + 1).bit_length() == 32 and platform.machine() == 'x86_64':
    # Building 32-bit pyq on a 64-bit host
    config_vars = sysconfig.get_config_vars()
    CFLAGS.append('-m32')
    LDFLAGS.append('-m32')

    def split_replace(string, a, b, sep):
        x = string.split(sep)
        for i, part in enumerate(x):
            if part == a:
                x[i] = b
        return sep.join(x)

    for k, v in config_vars.items():
        if isinstance(v, str):
            config_vars[k] = split_replace(v, 'x86_64', 'i386', '-')

TEST_REQUIREMENTS = [
                        'pytest>=2.6.4,!=3.2.0,!=3.3.0',
                        'pytest-pyq',
                        'pytest-cov>=2.4',
                        'coverage>=4.2'
                    ] + (['pathlib2>=2.0'] if sys.version_info[0] < 3 else [])

IPYTHON_REQUIREMENTS = ['ipython']

Executable = Extension

METADATA = dict(
    name='pyq',
    packages=['pyq', 'pyq.tests', ],
    package_dir={'': 'src'},
    qlib_scripts=['python.q', 'p.k', 'pyq-operators.q', 'pyq-print.q', ],
    ext_modules=[
        Extension('pyq._k', sources=['src/pyq/_k.c', ],
                  extra_compile_args=CFLAGS,
                  extra_link_args=LDFLAGS),
    ],
    qext_modules=[
        Extension('pyq', sources=['src/pyq/pyq.c', ],
                  extra_compile_args=CFLAGS,
                  extra_link_args=LDFLAGS),
    ],
    executables=[] if WINDOWS else [
        Executable('pyq', sources=['src/pyq.c'],
                   extra_compile_args=CFLAGS,
                   extra_link_args=LDFLAGS),
    ],
    scripts=['src/scripts/pyq-runtests',
             'src/scripts/pyq-coverage',
             'src/scripts/ipyq',
             'src/scripts/pq',
             'src/scripts/qp',
             ],
    data_files=[
        ('q', ['src/pyq/p.k',
               'src/pyq/pyq-operators.q',
               'src/pyq/python.q',
               ]
         ),
    ],
    url='https://github.com/KxSystems/pyq',
    maintainer='PyQ Authors',
    maintainer_email='pyq@enlnt.com',
    license='Apache License',
    platforms=['Linux', 'MacOS X', 'Windows'],
    classifiers=['Development Status :: 5 - Production/Stable',
                 'Environment :: Console',
                 'Intended Audience :: Developers',
                 'Intended Audience :: Financial and Insurance Industry',
                 'Intended Audience :: Science/Research',
                 'License :: OSI Approved :: Apache Software License',
                 'Natural Language :: English',
                 'Operating System :: MacOS :: MacOS X',
                 'Operating System :: POSIX :: Linux',
                 'Operating System :: Microsoft :: Windows :: Windows 10',
                 'Programming Language :: C',
                 'Programming Language :: Python :: 3.6',
                 'Programming Language :: Python :: 3.7',
                 'Programming Language :: Python :: Implementation :: CPython',
                 'Topic :: Database',
                 'Topic :: Software Development :: Libraries' +
                 ' :: Python Modules'],
)


def add_data_file(data_files, target, source):
    """Add an entry to data_files"""
    for t, f in data_files:
        if t == target:
            break
    else:
        data_files.append((target, []))
        f = data_files[-1][1]
    if source not in f:
        f.append(source)


def get_q_home(env):
    """Derive q home from the environment"""
    q_home = env.get('QHOME')
    if q_home:
        return q_home
    for v in ['VIRTUAL_ENV', 'HOME']:
        prefix = env.get(v)
        if prefix:
            q_home = os.path.join(prefix, 'q')
            if os.path.isdir(q_home):
                return q_home
    if WINDOWS:
        q_home = os.path.join(env['SystemDrive'], r'\q')
        if os.path.isdir(q_home):
            return q_home
    raise RuntimeError('No suitable QHOME.')


def get_q_os_letter(sysname, machine):
    if sysname == 'Linux':
        return 'l'
    if sysname == 'SunOS':
        return 'v' if machine == 'i86pc' else 's'
    if sysname == 'Darwin':
        return 'm'
    if sysname == 'Windows':
        return 'w'
    raise RuntimeError('"Unknown platform: %s %s.' % (sysname, machine))


def get_q_arch(q_home):
    bits = (sys.maxsize + 1).bit_length()
    sysname = platform.system()
    machine = platform.machine()

    os_letter = get_q_os_letter(sysname, machine)
    if bits == 64:
        # In case we're on 64-bit platform, but 64-bit kdb+ is not available
        # we will fallback to the 32-bit version.
        x64dir = os.path.join(q_home, '%s64' % os_letter)
        if not os.path.isdir(x64dir):
            bits = 32
    return '%s%d' % (os_letter, bits)


def get_q_version(q_home):
    """Return version of q installed at q_home"""
    with open(os.path.join(q_home, 'q.k')) as f:
        for line in f:
            if line.startswith('k:'):
                return line[2:5]
    return '2.2'


decode = (lambda x: x) if str is bytes else lambda x: x.decode()


def get_python_dll(executable):
    sysname = platform.system()
    if sysname.startswith(('Linux', 'SunOS')):
        output = subprocess.check_output(['ldd', executable])
        for line in output.splitlines():
            if b'libpython' in line:
                return decode(line.split()[2])

        # This is for systems which have statically linked Python
        # (i.e Ubuntu), but provide dynamic libraries in a separate
        # package.
        libpython = 'libpython{}.{}'.format(*sys.version_info[:2]).encode()
        try:
            output = subprocess.check_output(['ldconfig', '-p'])
        except subprocess.CalledProcessError:
            output = subprocess.check_output(['/sbin/ldconfig', '-p'])
        for line in output.splitlines():
            if libpython in line:
                return decode(line.split()[-1])

    elif sysname == 'Darwin':
        output = subprocess.check_output(['otool', '-L', executable])
        for line in output.splitlines()[1:]:
            if b'Python' in line:
                python_dll = decode(line.split()[0])
                return python_dll.replace('@executable_path',
                                          os.path.dirname(executable))
    elif sysname == 'Windows':
        return 'python{}{}.dll'.format(*sys.version_info[:2])
    # This is known to work for Anaconda
    ldlibrary = sysconfig.get_config_var('LDLIBRARY')
    libdir = sysconfig.get_config_var('LIBDIR')
    if ldlibrary and libdir:
        libfile = os.path.join(libdir, ldlibrary)
        if os.path.exists(libfile):
            return libfile
    raise RuntimeError('no python dll')


SETUP_CFG = """\
[config]
q_home = {q_home}
q_version = {q_version}
q_arch = {q_arch}
python_dll = {python_dll}
"""


class Config(config):
    user_options = [
        ('q-home=', None, 'q home directory'),
        ('q-version=', None, 'q version'),
        ('q-arch=', None, 'q architecture, e.g. l64'),
        ('python-dll=', None, 'path to the python dynamic library'),
        ('dest=', None, "path to the config file (default: setup.cfg)"),
        ('write', None, 'write the config file')
    ]

    q_home = None
    q_arch = None
    q_version = None
    python_dll = None
    dest = None
    write = None

    extra_link_args = []

    def initialize_options(self):
        config.initialize_options(self)

    def finalize_options(self):
        if self.q_home is None:
            self.q_home = get_q_home(os.environ)
        if self.q_arch is None:
            self.q_arch = get_q_arch(self.q_home)
        if self.q_version is None:
            self.q_version = get_q_version(self.q_home)
        if self.python_dll is None:
            self.python_dll = get_python_dll(sys.executable)
        if self.dest is None:
            self.dest = 'setup.cfg'
        if WINDOWS:
            self.extra_link_args = [r'src\pyq\kx\%s\q.lib' % self.q_arch]

    def run(self):
        setup_cfg = SETUP_CFG.format(**vars(self))
        self.announce(setup_cfg.rstrip(), 2)
        if self.write:
            with open(self.dest, 'w') as f:
                f.write(setup_cfg)
            self.announce('^^^ Written to %s.' % self.dest, 2)
        else:
            self.announce('^^^ Use --write options'
                          ' to write this to %s.' % self.dest, 2)


PYQ_CONFIG = """\
\\d .pyq
python_dll:"{python_dll}\\000"
pyq_executable:"{pyq_executable}"
"""


class BuildQLib(Command):
    description = "build q/k scripts"

    user_options = [
        ('build-lib=', 'd', "build directory"),
        ('force', 'f', "forcibly build everything (ignore file timestamps)"),
    ]

    q_home = None
    build_base = None
    build_lib = None

    python_dll = None
    pyq_executable = None

    def initialize_options(self):
        pass

    def finalize_options(self):
        self.set_undefined_options('config',
                                   ('q_home', 'q_home'),
                                   ('python_dll', 'python_dll'))
        self.set_undefined_options('build',
                                   ('build_base', 'build_base'))
        self.build_lib = os.path.join(self.build_base, 'qlib')
        cmd = self.get_finalized_command('install_exe')
        pyq_path = os.path.join(cmd.install_dir, 'pyq')
        self.pyq_executable = pyq_path.replace('\\', '\\\\')

    def run(self):
        self.mkpath(self.build_lib)
        for script in self.distribution.qlib_scripts:
            outfile = os.path.join(self.build_lib, script)
            script_file = os.path.join('src', 'pyq', script)
            self.write_pyq_config()
            self.copy_file(script_file, outfile, preserve_mode=0)

    def write_pyq_config(self):
        pyq_config_file = os.path.join(self.build_lib, 'pyq-config.q')
        with open(pyq_config_file, 'w') as f:
            f.write(PYQ_CONFIG.format(**vars(self)))
        add_data_file(self.distribution.data_files, 'q', pyq_config_file)


class BuildQExt(Command):
    description = "build q extension modules"

    user_options = [
        ('build-lib=', 'd', "build directory"),
        ('force', 'f', "forcibly build everything (ignore file timestamps)"),
    ]

    q_home = None
    q_arch = None
    q_version = None

    build_base = None
    build_temp = None
    build_lib = None

    compiler = None
    define = None
    debug = None
    force = None
    plat_name = None

    extensions = None

    def initialize_options(self):
        pass

    def finalize_options(self):
        self.set_undefined_options('config',
                                   ('q_home', 'q_home'),
                                   ('q_arch', 'q_arch'),
                                   ('q_version', 'q_version'))
        self.set_undefined_options('build',
                                   ('build_base', 'build_base'),
                                   ('compiler', 'compiler'),
                                   ('debug', 'debug'),
                                   ('force', 'force'),
                                   ('plat_name', 'plat_name'))
        if self.build_lib is None:
            self.build_lib = os.path.join(self.build_base,
                                          'qext.' + self.plat_name)
        if self.build_temp is None:
            self.build_temp = os.path.join(self.build_base,
                                           'temp.' + self.plat_name)
        if self.extensions is None:
            self.extensions = self.distribution.qext_modules
        if self.define is None:
            split_version = self.q_version.split('.')
            self.define = [('KXVER', split_version[0]),
                           ('KXVER2', split_version[1]), ]

    def run(self):
        from distutils.ccompiler import new_compiler
        from distutils.sysconfig import customize_compiler

        include_dirs = ['src/pyq/kx', ]

        conf = self.get_finalized_command("config")
        for ext in self.extensions:
            sources = ext.sources
            ext_path = os.path.join(self.build_lib,
                                    ext.name + ('.dll' if WINDOWS else '.so'))
            compiler = new_compiler(compiler=self.compiler,
                                    verbose=self.verbose,
                                    dry_run=self.dry_run,
                                    force=self.force)
            customize_compiler(compiler)
            if WINDOWS:
                compiler.initialize()
                compiler.compile_options.remove('/MD')
            extra_args = ext.extra_compile_args or []
            objects = compiler.compile(sources,
                                       output_dir=self.build_temp,
                                       macros=self.define,
                                       extra_postargs=extra_args,
                                       include_dirs=include_dirs)
            extra_args = conf.extra_link_args[:] + ext.extra_link_args
            if WINDOWS:
                extra_args.extend([r'/DEF:src\pyq\%s.def' % ext.name])

            compiler.link_shared_object(objects, ext_path,
                                        extra_postargs=extra_args)
            add_data_file(self.distribution.data_files,
                          os.path.join('q', self.q_arch), ext_path)


class BuildPyExt(build_ext):
    q_arch = None

    def finalize_options(self):
        build_ext.finalize_options(self)
        self.set_undefined_options('build_qext',
                                   ('define', 'define'))
        self.set_undefined_options('config',
                                   ('q_arch', 'q_arch'))
        conf = self.get_finalized_command("config")
        if conf.extra_link_args:
            for ext in self.extensions:
                ext.extra_link_args = [a.format(**vars(ext))
                                       for a in conf.extra_link_args]

    if WINDOWS:
        def build_extensions(self):
            self.compiler.initialize()
            self.compiler.compile_options.remove('/MD')
            build_ext.build_extensions(self)


class BuildExe(Command):
    description = "build executables"
    user_options = []

    q_home = None
    q_arch = None
    q_version = None

    build_temp = None
    build_exe = None
    build_base = None

    compiler = None
    debug = None
    define = None
    plat_name = None

    def initialize_options(self):
        pass

    def finalize_options(self):
        self.set_undefined_options('config',
                                   ('q_home', 'q_home'),
                                   ('q_arch', 'q_arch'),
                                   ('q_version', 'q_version'))
        self.set_undefined_options('build',
                                   ('build_base', 'build_base'),
                                   ('compiler', 'compiler'),
                                   ('debug', 'debug'),
                                   ('force', 'force'),
                                   ('plat_name', 'plat_name'))

        if self.build_exe is None:
            self.build_exe = os.path.join(self.build_base,
                                          'exe.{}-{}'.format(self.plat_name,
                                                             sys.version[:3]))
        if self.define is None:
            self.define = [
                ('KXVER', self.q_version[0]),
                ('QARCH', self.q_arch),
            ]

    def run(self):
        from distutils.ccompiler import new_compiler
        from distutils.sysconfig import customize_compiler

        for exe in self.distribution.executables:
            compiler = new_compiler(
                compiler=self.compiler,
                verbose=self.verbose,
                dry_run=self.dry_run,
                force=self.force)
            customize_compiler(compiler)
            extra_args = exe.extra_compile_args or []
            objects = compiler.compile(exe.sources,
                                       macros=self.define,
                                       extra_postargs=extra_args,
                                       output_dir=self.build_temp)
            compiler.link_executable(objects,
                                     extra_preargs=LDFLAGS,
                                     output_progname=exe.name,
                                     output_dir=self.build_exe)


class InstallQLib(install_data):
    description = "install q/k scripts"

    build_dir = None
    skip_build = None
    outfiles = None

    def finalize_options(self):
        self.set_undefined_options('config', ('q_home', 'install_dir'))
        self.set_undefined_options('build_qlib', ('build_lib', 'build_dir'))
        self.set_undefined_options('install', ('skip_build', 'skip_build'))

    def run(self):
        if not self.skip_build:
            self.run_command('build_qlib')
        self.outfiles = self.copy_tree(self.build_dir, self.install_dir)


class InstallQExt(install_data):
    description = "install q/k scripts"

    q_home = None
    q_arch = None
    build_dir = None
    skip_build = None
    install_dir = None
    outfiles = None

    def finalize_options(self):
        self.set_undefined_options('config',
                                   ('q_home', 'q_home'),
                                   ('q_arch', 'q_arch'))
        self.set_undefined_options('build_qext', ('build_lib', 'build_dir'))
        self.set_undefined_options('install', ('skip_build', 'skip_build'))
        self.install_dir = os.path.join(self.q_home, self.q_arch)

    def run(self):
        if not self.skip_build:
            self.run_command('build_qext')
        self.outfiles = self.copy_tree(self.build_dir, self.install_dir)


class InstallExe(install_scripts):
    description = "install executables"

    outfiles = None

    def finalize_options(self):
        self.set_undefined_options('build_exe', ('build_exe', 'build_dir'))
        self.set_undefined_options('install',
                                   ('install_scripts', 'install_dir'),
                                   ('force', 'force'),
                                   ('skip_build', 'skip_build'),
                                   )

    def run(self):
        if not self.skip_build:
            self.run_command('build_exe')
        from stat import ST_MODE
        if not self.get_inputs():
            return
        self.outfiles = self.copy_tree(self.build_dir, self.install_dir)
        if os.name == 'posix':
            # Set the executable bits (owner, group, and world) on
            # all the executables we just installed.
            for file in self.get_outputs():
                if self.dry_run:
                    self.announce("changing mode of %s" % file, 2)
                else:
                    mode = ((os.stat(file)[ST_MODE]) | 0o555) & 0o7777
                    self.announce("changing mode of %s to %o" %
                                  (file, mode), 2)
                    os.chmod(file, mode)

    def get_inputs(self):
        return self.distribution.executables or []


class PyqDistribution(Distribution):
    qlib_scripts = None
    qext_modules = None
    executables = None


build.sub_commands.extend([
    ('build_qlib', None),
    ('build_qext', None),
    ('build_exe', None),
])

install.sub_commands.extend([
    ('install_qlib', None),
    ('install_qext', None),
    ('install_exe', None),
])


def run_setup(metadata):
    summary, details = __doc__.split('\n\n', 1)
    with open('README.md') as f:
        long_description = f.read()
    keywords = metadata.copy()
    keywords.update(
        use_scm_version={'write_to': VERSION_FILE},
        description=summary,
        long_description=long_description,
        long_description_content_type='text/markdown',
        distclass=PyqDistribution,
        cmdclass={
            'config': Config,
            'build_qlib': BuildQLib,
            'build_qext': BuildQExt,
            'build_ext': BuildPyExt,
            'build_exe': BuildExe,
            'install_qlib': InstallQLib,
            'install_qext': InstallQExt,
            'install_exe': InstallExe,
        },
    )
    if 'setuptools' in sys.modules:
        keywords['extras_require'] = {
            'test': TEST_REQUIREMENTS,
            'ipython': IPYTHON_REQUIREMENTS,
            'all': TEST_REQUIREMENTS + IPYTHON_REQUIREMENTS + [
                'py', 'numpy', 'prompt-toolkit', 'pygments-q'],
        }
        keywords['setup_requires'] = ['setuptools_scm']

    setup(**keywords)


if __name__ == '__main__':
    run_setup(METADATA)
