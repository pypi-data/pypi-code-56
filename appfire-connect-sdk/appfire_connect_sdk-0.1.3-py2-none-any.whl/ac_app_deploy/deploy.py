#
#  Copyright (c) 2020 Appfire Technologies, Inc.
#  All rights reserved.
#  This software is licensed under the provisions of the "Bob Swift Atlassian Add-ons EULA"
#  (https://bobswift.atlassian.net/wiki/x/WoDXBQ) as well as under the provisions of
#  the "Standard EULA" from the "Atlassian Marketplace Terms of Use" as a "Marketplace Product”
#  (http://www.atlassian.com/licensing/marketplace/termsofuse).
#  See the LICENSE file for more details.
#

import json
import logging
import subprocess
import sys
import click
import yaml


@click.command()
@click.option('--verbose', '-v', is_flag=True, help="Verbose output")
@click.option('--profile', '-p', help="AWS profile as the default environment", default="default")
@click.option('--env', '-e', help="standalone, dts or prod", default="standalone")
@click.option('--stack', '-s', help="CDK stack to deploy", default="app")
@click.option('--stage', '-stage', help="dev, test, stage or prod", default="dev")
@click.option('--app-suffix', '-as', help="blue or green", default="blue")
@click.argument('command')
def process(verbose, command, profile, env, stage, stack, app_suffix):
    """
    gathers information related to deployment and deploys the CDK stack
    """
    log_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=log_level, stream=sys.stdout, format="%(message)s")
    logger = logging.getLogger("ac_app_deploy")
    logger.debug("checking environment " + env)
    if env == 'standalone':
        personal_env_settings = None
        try:
            with open("./personal.env.yml", 'r') as stream:
                    personal_env_settings = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            logger.info(exc)
        except IOError:
            logger.info("personal.env.yml not found!")
        aws_profile = profile if profile else personal_env_settings['environment']['personal']['profile']
        domain = personal_env_settings['environment']['personal']['domain']
        log_info(logger, aws_profile, domain, env)
    elif env == 'dts':
        dts_env_settings = None
        try:
            with open("./env.yml", 'r') as stream:
                dts_env_settings = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
                logger.info(exc)
        except IOError:
                logger.info("env.yml not found!")
        aws_profile = profile if profile else dts_env_settings['environment'][env][stage]['profile']
        domain = dts_env_settings['environment'][env][stage]['domain']
        log_info(logger, aws_profile, domain, env)
    else:
        prod_env_settings = None
        try:
            with open("./env.yml", 'r') as stream:
                prod_env_settings = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            logger.info(exc)
        except IOError:
            logger.info("env.yml not found!")
        aws_profile = profile if profile else prod_env_settings['environment'][env]['profile']
        domain = prod_env_settings['environment'][env]['domain']
        log_info(logger, aws_profile, domain, env)
    
    if command == 'bootstrap':
        shell(logger, "cdk bootstrap", raise_error=True)
    if command == 'deploy':
        # DTS GREEN: xxx-green-dev.dts-bobswift.appfire.app
        # DTS BLUE: xxx-dev.dts-bobswift.appfire.app
        # STANDALONE: xxx-dev.bobswift.lavadukanam.com
        # PROD: markdown.bobswift.appfire.app

        app_domain = domain.split(".")[2] + "." + domain.split(".")[3] if env == 'standalone' else "appfire.app"
        app_name = domain.split(".")[0].split("-")[0]
        brand = domain.split(".")[1] if env != 'standalone' else "bobswift"
        print(brand)
        print(domain.split("."))
        app_suffix = 'green' if app_suffix == 'green' else ''
        
        logger.debug("generating base url for atlassian-connect.json")
        generate_base_url(logger, "web/static/atlassian-connect.json", app_suffix, domain, env)
        generate_base_url(logger, "atlassian-connect.json", app_suffix, domain, env)
        logger.debug("overriding cdk.json with supplied arguments")
        generate_cdk_json(logger, app_suffix, app_domain, env, stack, stage, brand, app_name)
        if stack == 'core':
            shell(logger, "cdk deploy '*' --app 'npx ts-node ./node_modules/ac-core/bin/ac-core.js " + app_name + " " + stage
                                + " " + app_domain + " web/static " + brand + " " + env + " true " + app_suffix + "'" +
                  " --require-approval never --profile " + aws_profile, raise_error=True)
        else:
            shell(logger, "cdk deploy '*' --profile " + aws_profile, raise_error=True)
    elif command == 'diff':
        shell(logger, "cdk diff --profile " + aws_profile, raise_error=True)
    elif command == 'synth':
        shell(logger, "cdk synth --profile " + aws_profile, raise_error=True)
    elif command == 'destroy':
        shell(logger, "cdk destroy " + stack + "--profile " + aws_profile, raise_error=True)
    else:
        shell(logger, "cdk list --profile " + aws_profile, raise_error=True)


def generate_cdk_json(logger, app_suffix, app_domain, env, stack, stage, brand, app_name):
    '''dynamically prepare cdk.json based on command line arguments'''
    
    try:
        with open('cdk.json', 'r') as file:
            json_data = json.load(file)
            for item in json_data:
                if item == 'app':
                    json_data[
                        item] = "npx ts-node ./node_modules/ac-app-dist/bin/ac-app-dist.js " + app_name + " " + stage \
                                + " " + app_domain + " web/static " + brand + " " + env + " false " + app_suffix
        with open('cdk.json', 'w') as file:
            json.dump(json_data, file, indent=2)
    except IOError:
        shell(logger, "cdk.json not found!")


def generate_base_url(logger, path, app_suffix, domain, env):
    '''generate baseurl in atlassian-connect descriptor'''
    
    try:
        with open(path, 'r') as file:
            json_data = json.load(file)
            for item in json_data:
                if item == 'baseUrl':
                    if env == 'dts':
                        app_name = domain.split(".")[0].split("-")[0]
                        env_stage = domain.split(".")[0].split("-")[1]
                        domain = domain if app_suffix != 'green' else app_name + "-green-" + env_stage + "." + \
                                                                      domain.split(".")[1] + "." + \
                                                                      domain.split(".")[2] + "." + \
                                                                      domain.split(".")[3]
                    if env == 'prod':
                        app_name = domain.split(".")[0]
                        domain = domain if app_suffix != 'green' else app_name + "-green." + \
                                                                      domain.split(".")[1] + "." + \
                                                                      domain.split(".")[2] + "." + \
                                                                      domain.split(".")[3]
                    
                    json_data[item] = "https://" + domain
                if item == 'links':
                    json_data['links']['self'] = "https://" + domain + "/atlassian-connect.json"
        
        with open(path, 'w') as file:
            json.dump(json_data, file, indent=2)
    except IOError:
        shell(logger, path + " not found!")


def log_info(logger, aws_profile, domain, env):
    logger.info(f'Environment: {env}')
    logger.info(f'AWS Profile: {aws_profile}')
    logger.info(f'Domain: {domain}')

def shell(logger, cmd, raise_error=False):
    """
    Run a shell command.
    :param logger:
    :param cmd:  Shell line to be executed
    :param raise_error:
    :return: Tuple (return code, interleaved stdout and stderr output as string)
    """
    
    logger.debug("Running : %s" % cmd)
    process = subprocess.run(
        cmd,
        check=True,
        shell=True
    )
    if raise_error and process.returncode != 0:
        logger.error("Command output:")
        raise ShellCommandFailed("The following command did not succeed: %s" % cmd)
    
    return (process.returncode)


class ShellCommandFailed(Exception):
    """ Executing a shell command failed """


if __name__ == "__main__":
    process()
