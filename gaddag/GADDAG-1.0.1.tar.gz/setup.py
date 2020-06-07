from setuptools import setup, Extension
from distutils.command.build_ext import build_ext


class build_ext(build_ext):
    def build_extension(self, ext):
        self._ctypes = isinstance(ext, CTypes)
        return super().build_extension(ext)

    def get_export_symbols(self, ext):
        if self._ctypes:
            return ext.export_symbols
        return super().get_export_symbols(ext)

    def get_ext_filename(self, ext_name):
        if self._ctypes:
            return ext_name + '.so'
        return super().get_ext_filename(ext_name)


class CTypes(Extension):
    pass


with open("README.md") as f:
    readme = f.read()

libcgaddag = CTypes(
    "gaddag/libcgaddag",
    sources=["gaddag/cGADDAG-1.0/src/cgaddag.c"],
    extra_compile_args=[
        "-DCOMPRESSION",
        "-I./gaddag/cGADDAG-1.0/include",
        "-fPIC",
        "-O3",
    ],
    extra_link_args=["-lz"],
)

setup(
    name="GADDAG",
    version="1.0.1",
    description="Python wrapper around cGADDAG",
    long_description=readme,
    long_description_content_type="text/markdown",
    license="MIT",
    author="Jordan Bass",
    author_email="jordan@jbass.io",
    url="https://git.sr.ht/~jorbas/GADDAG",
    download_url="https://git.sr.ht/~jorbas/GADDAG/archive/1.0.1.tar.gz",
    platforms="any",
    python_requires='>=3',
    packages=["gaddag"],
    ext_modules=[libcgaddag],
    tests_require=["pytest"],
    cmdclass={"build_ext": build_ext},
    classifiers=[],
)
