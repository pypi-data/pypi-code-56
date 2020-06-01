from setuptools import setup, find_packages

setup(name='ddclassification',
      version='0.1.3',
      url='https://github.com/ddcloud-uiyunkim/ddclassification',
      license='MIT',
      author='Uiyun Kim',
      author_email='uiyunkim@kakao.com',
      description='general image classification library',
      packages=find_packages(),
      long_description=open('README.md').read(),
      zip_safe=False,
      #install_requires=['tensorflow-gpu'],
    )