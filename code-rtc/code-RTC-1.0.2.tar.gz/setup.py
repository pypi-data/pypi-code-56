from setuptools import find_packages, setup
import code_rtc
setup(
    name='code-RTC',
    version='1.0.2',
    author='PSKP-95',
    author_email="patil8698parikshit@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'flask_cors',
        'pymysql'
    ],
    entry_points={
        'console_scripts': [
            'code-rtc=code_rtc.app:main'
        ],
    }
)