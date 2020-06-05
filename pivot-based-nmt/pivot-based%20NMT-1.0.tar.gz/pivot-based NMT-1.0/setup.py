from setuptools import setup, find_packages
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='pivot-based NMT',
      description='a zero-shot NMT',
      long_description=long_description,
      long_description_content_type='text/markdown',
      version='1.0',
      packages=find_packages(),
      project_urls={"source": "https://github.com/dotaofll/Teacher-Student"},
      install_requires=["OpenNMT-py"],
      entry_points={
          "console_scripts": [
              "my_train=ZSMT.bin.train:main",
              "my_preprocess=ZSMT.bin.preprocess:main",
              "my_pre_pipline=ZSMT.bin.pre_pipeline:main",
              "my_bpe_learn=ZSMT.bin.learn_bpe:main",
              "my_apply_bpe=ZSMT.bin.apply_bpe:main",
              "my_translate=ZSMT.bin.translate:main"
          ]
      })
