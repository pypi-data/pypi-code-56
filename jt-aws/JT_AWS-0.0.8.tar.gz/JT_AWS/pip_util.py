import pip


def InstallRequirements(requirements_path, target_path):
    """
    Installs all the packages for an AWS Lambda function.

    This function tries to install the version of a package built for the specific operating system that AWS Lambda functions run on

    :param requirements_path: Path to the requirements file
    :param target_path: Path to the folder where the requirements 
    :return:
    """
    with open(requirements_path) as _:
        requirements = _.readlines()

    for requirement in requirements:
        result = pip.main([
            'install',
            '-q',
            '--platform=manylinux1_x86_64',
            f'--target={target_path}',
            '--only-binary=:all:',
            '--upgrade',
            requirement
        ])
        if result:
            pip.main(['install', '-q', f'--target={target_path}', '--upgrade', requirement])
