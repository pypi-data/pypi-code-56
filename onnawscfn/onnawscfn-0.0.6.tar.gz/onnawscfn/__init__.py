"""Convenience Python module for AWS CloudFormation

## Example

    from onnlogger import Loggers
    from pprint import pprint

    # Create a `Loggers` object and pass it into `Cfn`
    logger = Loggers(logger_name='Cfn', console_logger=True, log_level='INFO', log_file_path='/tmp/log')
    cfn = Cfn(logger)

    # Convert a `dict` to CloudFormation parameters:
    params = {
    'AccountId': '123456789012',
    'ExternalId': '098765432109',
    }

    cfn_params = cfn.dict_to_cfn_params(params)
    pprint(cfn_params)
    [{'ParameterKey': 'AccountId', 'ParameterValue': '123456789012'},
    {'ParameterKey': 'ExternalId', 'ParameterValue': '098765432109'}]

## Installation

    pip3 install onnawscfn

## Contact

* Code: [onnawscfn](https://github.com/OzNetNerd/onnawscfn)
* Blog: [oznetnerd.com](https://oznetnerd.com)
* Email: [will@oznetnerd.com](mailto:will@oznetnerd.com)

"""

from .cfn import Cfn