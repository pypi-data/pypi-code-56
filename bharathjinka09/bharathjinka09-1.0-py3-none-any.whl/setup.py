from distutils.core import setup

setup(
    name = 'zipcode_to_map',
    packages = ['zipcode_to_map'],
    version = '1.0',  # Ideally should be same as your GitHub release tag varsion
    description = 'Provide a Country code and postal code.It will generate a map in a html file based on these details.Used pgeocode and folium packages.',
    author = 'JINKA RANGA BHARATH',
    author_email = 'bharathjinka09@gmail.com',
    url = 'https://github.com/bharathjinka09/zipcode_to_map',
    download_url = 'https://github.com/bharathjinka09/zipcode_to_map/archive/1.0.tar.gz',
    keywords = ['zipcode', 'HTML map file'],
    classifiers = [],
)