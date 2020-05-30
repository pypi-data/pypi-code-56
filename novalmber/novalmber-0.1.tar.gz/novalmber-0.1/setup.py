from setuptools import setup,find_packages
setup(name='novalmber',
      version='0.1',
      description='A plugin interface and developer package for NovalIDE.',
      url='https://gitee.com/hzy15610046011/TakagiABM',
      author='Zhanyi Hou',
      author_email='3120388018@qq.com',
      license='MuLan2.0',
      packages=find_packages(),
      include_package_data = True

      )#package_data={'':['hat.png']})
     # zip_safe=False,install_requires = ['pyqt5','pyqtgraph','numpy','pyopengl'])
