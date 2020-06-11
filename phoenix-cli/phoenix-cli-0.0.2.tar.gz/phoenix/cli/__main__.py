import sys
from knack import CLI
from . import PxCliCommandLoader, PxCLIHelp

pxcli = CLI(cli_name='px', commands_loader_cls=PxCliCommandLoader, help_cls=PxCLIHelp)
exit_code = pxcli.invoke(sys.argv[1:])
