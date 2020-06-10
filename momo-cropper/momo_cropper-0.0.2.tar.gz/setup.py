# coding=utf8
import setuptools

setuptools.setup(
    name='momo_cropper',
    version='0.0.2',
    keywords=('cropper', 'image'),
    description='An image cropping tool by given border colors.',
    license='MIT licence',
    url='',
    author='Momo',
    author_email='1447340425@qq.com',
    packages=setuptools.find_packages(),
    py_modules=['cropper'],
    platforms='any',
    install_requires = [
        'opencv-python==4.2.0.34',
        'numpy==1.18.4',
        'pillow==7.1.2',
        'setuptools==47.1.1',
    ],
    entry_points={
        'console_scripts': [
            'cropper = cropper:main'
        ]
    }
)
