###                 PACKAGEUPLOAD
### 
### by Anime no Sekai
### 2020
### 
### v.1.5


import lifeeasy
import filecenter
import random
import json

# var declaration
package_name = ''
main_module = ''
customclassifiers_bool = True
upgrade = False
custom_setup = False

def start(keepsetup=False, cleanup=True, customclassifiers=True, customurl=False, upgrade=False, customsetup=False):
    global customclassifiers_bool
    global custom_setup
    custom_setup = customsetup
    customclassifiers_bool = customclassifiers
    lifeeasy.clear()
    status = first_confirmation()
    if status == 0:
        status = detect_setup(customurl=customurl, upgrade=upgrade)
        lifeeasy.clear()
        if status == 0:
            status = module_verification()
            lifeeasy.clear()
            if status == 0:
                status = build()
                lifeeasy.clear()
                if status == 0:
                    status = upload()
                    lifeeasy.clear()
                    if status == 0:
                        if cleanup == True:
                            status = clean(keepsetup=keepsetup)
                            lifeeasy.clear()
                            if status == 0:
                                print('Do you want to install the package?')
                                user_choice = input('[enter] to install or enter [quit] ')
                                if user_choice.lower() != 'quit' and user_choice.lower() != 'stop' and user_choice.lower() != 'no':
                                    status = download()
                                    if status == 0:
                                        print('Everything is ok!')
                                        return 0
                                    else:
                                        print('An error occured while downloading the package.')
                                        return 7
                                else:
                                    print('Everything is ok!')
                                    return 0
                            else:
                                print('An error occured while cleaning up the package directory.')
                                return 1
                        else:
                            print('Everything is ok!')
                            return 0
                    else:
                        print('An error occured while uploading your package.')
                        return 2
                else:
                    print('An error occured while building the package.')
                    return 3
            else:
                print('An error occured while verifying the module.')
                return 4
        else:
            print('An error occured while creating your setup file.')
            return 5
    else:
        print('Ok!')
        return 6

def first_confirmation():
    print('Make sure to have your package uploaded to GitHub')
    lifeeasy.sleep(1)
    print('Make sure to make a release of this package on GitHub')
    lifeeasy.sleep(1)
    print('')
    print('')
    user_choice = input('Press [enter] to coninue or enter [quit] to abort...')
    if user_choice.lower() == "quit":
        return 1
    else:
        return 0

def detect_setup(customurl, upgrade):
    if filecenter.exists(lifeeasy.working_dir() + '/setup.py'):
        print('setup.py detected')
        return 0
    else:
        return setup(customurl=customurl, force_upgrade=upgrade)
        
def module_verification():
    global main_module
    global package_name
    if package_name == '':
        print('What is the name of the module that you want to verify/package?')
        package_name = input('> ')
    try:
        lifeeasy.display_action('Verification of the module', delay=0.1)
        if filecenter.isdir(lifeeasy.working_dir() + '/' + package_name):
            if filecenter.isfile(lifeeasy.working_dir() + '/' + package_name + '/__init__.py'):
                main_module = '__init__.py'
                print("It's all good!")
            else:
                if filecenter.isfile(lifeeasy.working_dir() + '/__init__.py'):
                    main_module = '__init__.py'
                    for file in filecenter.files_in_dir(lifeeasy.working_dir()):
                        if file == 'setup.py':
                            continue
                        if filecenter.extension_from_base(file) == '.py':
                            filecenter.move(lifeeasy.working_dir() + file, lifeeasy.working_dir() + '/' + package_name + '/' + file)
                else:
                    init_file = input('Write the name of the main module file (with the extension): ')
                    main_module = init_file
                    filecenter.move(lifeeasy.working_dir() + '/' + init_file, lifeeasy.working_dir() + '/' + package_name + '/__init__.py')
                    for file in filecenter.files_in_dir(lifeeasy.working_dir()):
                        if file == 'setup.py':
                            continue
                        if filecenter.extension_from_base(file) == '.py':
                            filecenter.move(lifeeasy.working_dir() + file, lifeeasy.working_dir() + '/' + package_name + '/' + file)
            print('Make sure to move all the files used by your package in the folder "' + package_name + '"')
            input('Press [enter] to coninue...')
            
        else:
            filecenter.make_dir(lifeeasy.working_dir() + '/' + package_name)
            if filecenter.isfile(lifeeasy.working_dir() + '/__init__.py'):
                main_module = '__init__.py'
                for file in filecenter.files_in_dir(lifeeasy.working_dir()):
                    if file == 'setup.py':
                        continue
                    if filecenter.extension_from_base(file) == '.py':
                        filecenter.move(lifeeasy.working_dir() + file, lifeeasy.working_dir() + '/' + package_name + '/' + file)
            else:
                init_file = input('Write the name of the main module file (with the extension): ')
                main_module = init_file
                filecenter.move(lifeeasy.working_dir() + '/' + init_file, lifeeasy.working_dir() + '/' + package_name + '/__init__.py')
                for file in filecenter.files_in_dir(lifeeasy.working_dir()):
                    if file == 'setup.py':
                        continue
                    if filecenter.extension_from_base(file) == '.py':
                        filecenter.move(lifeeasy.working_dir() + file, lifeeasy.working_dir() + '/' + package_name + '/' + file)
            print('Make sure to move all the files used by your package in the folder "' + package_name + '"')
            input('Press [enter] to coninue...')
        return 0
    except:
        return 1
                    


def setup(customurl=False, force_upgrade=False):
    global package_name
    global upgrade
    global custom_setup

    upgrade = force_upgrade

    setup = []

    # AUTHOR
    author = input('Who is the author? ')
    print('')

    def naming_package():
        global package_name
        global upgrade
        # NAME
        package_name = input("What's the name of your package? ")
        print('')

        lifeeasy.display_action('Verification', delay=0.1)
        name_verification = lifeeasy.request('https://pypi.org/project/' + package_name + '/', 'get')
        if name_verification.status_code == 404:
            print('The name is available!')
        elif name_verification.status_code == 200:
            request = lifeeasy.request('https://pypi.org/pypi/' + package_name + '/json', 'get')
            request_json = json.loads(request.text)
            if request_json['info']['author'] == author:
                print('upload mode: upgrade')
                print('Do you want to change some metadatas or keep them?')
                user_choice = input('press [enter] to continue with current metadatas or type [continue] to continue modifying the metadatas... ')
                if user_choice.lower() == 'continue' or user_choice.lower() == 'ontinue' or user_choice.lower() == 'cntinue' or user_choice.lower() == 'coninue' or user_choice.lower() == 'contnue' or user_choice.lower() == 'contiue' or user_choice.lower() == 'contine' or user_choice.lower() == 'continu':
                    upgrade = False
                else:
                    upgrade = True
            else:
                print('This name is already taken!')
                print('Please try giving another name to the package...')
                print('')
                naming_package()
        else:
            print('An error occured with the name verification...')
            return 1

    if upgrade == False:
        if naming_package() == 1:
            return 1
    else:
        # NAME
        package_name = input("What's the name of your package? ")
        print('')

    # VERSION
    version = input("What's the version of " + package_name + '? ')
    print('')
        
    if upgrade == False:
        # DESCRIPTION
        print('Write a little summary/description of ' + package_name)
        desc = input('> ')
        print('')
        
        # EMAIL
        email = input('What is his ' + author + "'s email? ")
        print('')

        # LICENSE
        print('Warning: the license name is case-sensitive!')
        package_license = input('What is the license for ' + package_name + ' ? ')
        package_license_classifier = 'License :: OSI Approved :: ' + package_license + ' License'
        print('')

        request = lifeeasy.request('https://github.com/' + author + '/' + package_name, 'get')
        if request.status_code == 404:
            # GITHUB REPO
            print("What is the GitHub repository for this package?") 
            url = input('> ')
            print('')
        else:
            url = 'https://github.com/' + author + '/' + package_name
            
        # ARCHIVE
        if url[-1] == '/':
            download_url_try = url + 'archive/' + version + '.tar.gz'
        else:
            download_url_try = url + '/archive/' + version + '.tar.gz'
        request = lifeeasy.request(method='get', url=download_url_try)
        if request.status_code == 200:
            download_url = download_url_try
        else:
            if url[-1] == '/':
                download_url_try = url + 'archive/v' + version + '.tar.gz'
            else:
                download_url_try = url + '/archive/v' + version + '.tar.gz'
            request = lifeeasy.request(method='get', url=download_url_try)
            if request.status_code == 200:
                download_url = download_url_try
            else:
                github_release = input("What is the name of the GitHub release? ")
                print('')
                if url[-1] == '/':
                    download_url_try = url + 'archive/' + github_release + '.tar.gz'
                else:
                    download_url_try = url + '/archive/' + github_release + '.tar.gz'
                request = lifeeasy.request(method='get', url=download_url_try)
                if request.status_code == 200:
                    download_url = download_url_try
                else:
                    def ask_for_github_release():
                        global download_url
                        print('What is the URL of your GitHub release? (it ends with .tar.gz)')
                        download_url_try = input('> ')
                        print('')
                        request = lifeeasy.request(method='get', url=download_url_try)
                        if request.status_code == 200:
                            download_url = download_url_try
                        else:
                            print("It seems that you mistyped the URL or that the repository is private...")
                            lifeeasy.sleep(2)
                            print("Please put your GitHub repository visibility in public and retry...")
                            print('')
                            lifeeasy.sleep(2)
                            ask_for_github_release()
                    ask_for_github_release()

        # CUSTOM URL
        if customurl == True:
            print('What is the URL of the website for this package?')
            url = input('> ')
            print('')
            
        # KEYWORDS
        print('Enter a comma-separated list of keywords for your package')
        keywords = input('> ')
        keywords = keywords.split(',')
        print('')

        # DEPENDENCIES
        print('Enter a comma-separated list of dependencies for your package')
        dependencies = input('> ')
        dependencies = dependencies.replace(' ', '')
        dependencies = dependencies.split(',')
        print('')


        # PYTHON VERSIONS
        print('Enter a comma-separated list of supported Python version numbers for this package')
        print('(i.e 3,3.4,3.5,3.6,3.7,3.8)')
        python_versions = input('> ')
        print('')
        python_versions = python_versions.replace(' ', '')
        python_versions = python_versions.split(',')

        versions_classifiers = []
        for python_version in python_versions:
            versions_classifiers.append('Programming Language :: Python :: ' + python_version)


        dev_status = 'Development Status :: 4 - Beta'
        def development_status():
            global dev_status
            global customclassifiers_bool
            lifeeasy.clear()
            print('Choose a development status from the following')
            print('')
            print('Alpha')
            print('Beta')
            print('Stable')
            print('')
            print('Or press [enter] to add a custom one when adding classifiers...')
            print('')
            print('')
            dev_status_try = input('> ')

            if dev_status_try.lower() == 'alpha':
                dev_status = 'Development Status :: 3 - Alpha'
            elif dev_status_try.lower() == 'beta':
                dev_status = 'Development Status :: 4 - Beta'
            elif dev_status_try.lower() == 'stable':
                dev_status = 'Development Status :: 5 - Production/Stable'
            elif dev_status_try == '':
                customclassifiers_bool = True
            else:
                print("Sorry but I couldn't recognize the status.")
                lifeeasy.sleep(1)
                print('Please try again...')
                lifeeasy.sleep(1)
                development_status()
        development_status()

        # CUSTOM CLASSIFIERS
        custom_classifiers = []
        if customclassifiers_bool == True:
            lifeeasy.clear()
            print("What are the custom classifiers that you want to add?")
            print('')
            print("You need to enter your classifiers one-by-one")
            print("You need to write the full classifier")
            print("When you are done press [enter] again without entering anything.")
            print('')
            print('')
            user_choice = input('> ')
            if user_choice != '':
                custom_classifiers.append(user_choice)
            while user_choice != '':
                lifeeasy.clear()
                print("What are the custom classifiers that you want to add?")
                print('')
                print("You need to enter your classifiers one-by-one")
                print("You need to write the full classifier")
                print("When you are done press [enter] again without entering anything.")
                print('')
                print('')
                user_choice = input('> ')
                if user_choice != '':
                    custom_classifiers.append(user_choice)

    else:
        package_infos = lifeeasy.request('https://pypi.org/pypi/' + package_name + '/json', 'get')
        package_infos = json.loads(package_infos.text)
        package_license = package_infos['info']['license']
        desc = package_infos['info']['summary']
        author = package_infos['info']['author']
        email = package_infos['info']['author_email']
        url = package_infos['info']['home_page']
        download_url = package_infos['info']['download_url']
        keywords_string = package_infos['info']['keywords']
        keywords = keywords_string.split(',')
        dependencies = package_infos['info']['requires_dist']
        classifiers = package_infos['info']['classifiers']

    # CUSTOM SETUP

    if custom_setup == True:
        print('Add your custom setup sections (comma-separated)')
        setup_customized = input('> ')
        if len(setup_customized) == 0:
            custom_setup = False

    lifeeasy.clear()
    print('Building your setup file')
    lifeeasy.sleep(random.uniform(0.126, 0.31))


    print('adding imports')
    lifeeasy.sleep(random.uniform(0.126, 0.31))
    setup.append('from setuptools import setup')
    
    # README

    if filecenter.exists(lifeeasy.working_dir() + '/README.md'):
        print('adding the package readme')
        lifeeasy.sleep(random.uniform(0.126, 0.31))
        setup.append('from os import path')    
        setup.append("with open(path.join(path.abspath(path.dirname(__file__)), 'README.md'), encoding='utf-8') as f:")    
        setup.append("    readme_description = f.read()")

        long_description_type = 'text/markdown'

    elif filecenter.exists(lifeeasy.working_dir() + '/readme.md'):
        print('adding the package readme')
        lifeeasy.sleep(random.uniform(0.126, 0.31))
        setup.append('from os import path')  
        setup.append('')  
        setup.append("with open(path.join(path.abspath(path.dirname(__file__)), 'readme.md'), encoding='utf-8') as f:")    
        setup.append("    readme_description = f.read()")
        setup.append('')  
        setup.append('')  

        long_description_type = 'text/markdown'

    else:
        long_description_type = ''

    # Need to add more readme type

    print('creating the setup class')
    lifeeasy.sleep(random.uniform(0.126, 0.31))
    setup.append('setup(')

    print('adding the package name')
    lifeeasy.sleep(random.uniform(0.126, 0.31))
    setup.append('name = "' + package_name + '",')

    print('adding the packages name')
    lifeeasy.sleep(random.uniform(0.126, 0.31))
    setup.append('packages = ["' + package_name + '"],')

    print('adding the package version')
    lifeeasy.sleep(random.uniform(0.126, 0.31))
    setup.append('version = "' + version + '",')
    
    print('adding the package license')
    lifeeasy.sleep(random.uniform(0.126, 0.31))
    setup.append('license = "' + package_license + '",')
    
    print('adding the package description')
    lifeeasy.sleep(random.uniform(0.126, 0.31))
    setup.append('description = "' + desc + '",')
    
    print('adding the package author')
    lifeeasy.sleep(random.uniform(0.126, 0.31))
    setup.append('author = "' + author + '",')
    
    print('adding the package email')
    lifeeasy.sleep(random.uniform(0.126, 0.31))
    setup.append('author_email = "' + email + '",')
    
    print('adding the package url')
    lifeeasy.sleep(random.uniform(0.126, 0.31))
    setup.append('url = "' + url + '",')
    
    print('adding the package download url')
    lifeeasy.sleep(random.uniform(0.126, 0.31))
    setup.append('download_url = "' + download_url + '",')
    
    print('adding the package keywords')
    lifeeasy.sleep(random.uniform(0.126, 0.31))
    setup.append('keywords = ' +  str(keywords) + ',')
    
    print('adding the package dependencies')
    lifeeasy.sleep(random.uniform(0.126, 0.31))
    setup.append('install_requires = ' + str(dependencies) + ',')

    print('creating the package classifiers')
    lifeeasy.sleep(random.uniform(0.126, 0.31))
    if upgrade == False:
        classifiers = []
        classifiers.append(dev_status)
        classifiers.append(package_license_classifier)
        classifiers.extend(versions_classifiers)
        classifiers.extend(custom_classifiers)


    print('adding the package classifiers')
    lifeeasy.sleep(random.uniform(0.126, 0.31))
    setup.append('classifiers = ' + str(classifiers) + ',')
    
    print('adding the package readme')
    lifeeasy.sleep(random.uniform(0.126, 0.31))
    setup.append('long_description = readme_description,')

    print('adding the package readme type')
    lifeeasy.sleep(random.uniform(0.126, 0.31))
    setup.append('long_description_content_type = "' + long_description_type + '",')

    if custom_setup == True:
        print('adding your custom setup sections')
        lifeeasy.sleep(random.uniform(0.126, 0.31))
        setup.append(setup_customized)

    print('finishing...')
    lifeeasy.sleep(random.uniform(0.126, 0.31))
    setup.append(')')

    print('creating the file...')
    lifeeasy.write_file('setup.py', setup)
    lifeeasy.sleep(random.uniform(1.5, 2.3))
    return 0

def build():
    try:
        lifeeasy.display_action('Building the package', delay=0.1)
        print('')
        lifeeasy.command('python3 setup.py sdist bdist_wheel')
        return 0
    except:
        return 1

def upload():
    global package_name
    if package_name == '':
        print('What is the name of the package that you want to upload?')
        package_name = input('> ')
    try:
        print('')
        lifeeasy.display_action('Uploading the package', delay=0.1)
        lifeeasy.command('twine upload dist/*')
        print('')
        print('Package uploaded to PyPI!')
        print('Congratulations!')
        print('')
        print('Here is your link: https://pypi.org/project/' + package_name + '/')    
        return 0
    except:
        return 1

def clean(keepsetup=False):
    global package_name
    global main_module
    lifeeasy.display_action('Cleaning the package directory', delay=0.1)
    if package_name == '':
        package_name = input('What is the package name? ')
    if main_module == '':
        main_module = input('What is the main module file name (with extension) ? ')
    try:
        if filecenter.exists(lifeeasy.working_dir() + '/' + package_name + '.egg-info'):
            print('Removing .egg-info')
            filecenter.delete(lifeeasy.working_dir() + '/' + package_name + '.egg-info')
        if filecenter.exists(lifeeasy.working_dir() + '/dist'):
            print('Removing dist')
            filecenter.delete(lifeeasy.working_dir() + '/dist')
        if filecenter.exists(lifeeasy.working_dir() + '/build'):
            print('Removing build')
            filecenter.delete(lifeeasy.working_dir() + '/build')
        if filecenter.isdir(lifeeasy.working_dir() + '/' + package_name):
            print("Moving the package to its original location")
            for file in filecenter.files_in_dir(lifeeasy.working_dir() + '/' + package_name):
                print("Moving " + file)
                if file == '__init__.py':
                    filecenter.move(lifeeasy.working_dir() + '/' + package_name + '/' + file, lifeeasy.working_dir() + '/' + main_module)
                else:
                    filecenter.move(lifeeasy.working_dir() + '/' + package_name + '/' + file, lifeeasy.working_dir() + '/' + file)
        if filecenter.exists(lifeeasy.working_dir() + '/' + package_name):
            print('Deleting the package temp directory')
            filecenter.delete(lifeeasy.working_dir() + '/' + package_name)
        if filecenter.isfile(lifeeasy.working_dir() + '/setup.py'):
            if keepsetup == False:
                print('Deleting setup.py')
                filecenter.delete(lifeeasy.working_dir() + '/setup.py')
        if filecenter.isdir(lifeeasy.working_dir() + '/__pycache__'):
            print('Deleting caches')
            filecenter.delete(lifeeasy.working_dir() + '/__pycache__')
        return 0
    except:
        return 1

def download():
    global package_name
    if package_name == '':
        print('What is the name of the package that you want to install?')
        package_name = input('> ')
    try:
        if upgrade == False:
            lifeeasy.command('pip install ' + package_name)
        else:
            lifeeasy.command('pip install ' + package_name + ' --upgrade')
        return 0
    except:
        return 1