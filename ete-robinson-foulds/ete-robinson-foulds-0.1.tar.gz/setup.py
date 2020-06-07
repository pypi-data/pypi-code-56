from setuptools import setup

with open("README.md") as fh:
    long_description = fh.read()
    
if __name__ == '__main__':
    setup(name = 'ete-robinson-foulds',
          version = '0.1',
          description = 'implement Robinson Foulds Distance for ete.Tree structure',
          author = 'zhaofeng-shu33',
          author_email = '616545598@qq.com',
          url = 'https://github.com/zhaofeng-shu33/ete-robinson-foulds',
          maintainer = 'zhaofeng-shu33',
          maintainer_email = '616545598@qq.com',
          long_description = long_description,
          long_description_content_type="text/markdown",          
          install_requires = ['six'],
          license = 'Apache License Version 2.0',
          py_modules = ['ete_robinson_foulds'],
          classifiers = (
              "Development Status :: 4 - Beta",
              "Programming Language :: Python :: 3.7",
              "Operating System :: OS Independent",
          ),
    )