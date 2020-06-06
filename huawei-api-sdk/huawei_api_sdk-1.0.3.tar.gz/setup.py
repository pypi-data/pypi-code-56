try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

setup(name='huawei_api_sdk',     # 包名
      version='1.0.3',  # 版本号
      description='huawei api signature',
      long_description='huawei api signature',
      author='zhaoxiaolong',
      author_email='zhaoxiaolong@doodod.com',
      url='https://github.com/Drloveya/huawei_api_sdk',
      license='',
      install_requires=["requests", "aiohttp"],
      classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Natural Language :: Chinese (Simplified)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Utilities'
      ],
      keywords='',
      packages=find_packages(),  # 必填，就是包的代码主目录
      package_dir={},         # 必填
      include_package_data=True,
)

