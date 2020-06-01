
from cement import Controller
from cement.utils.version import get_version_banner
from ..core.version import get_version

VERSION_BANNER = """
Updates gh clie %s
%s
""" % (get_version(), get_version_banner())


class Base(Controller):
    class Meta:
        label = 'base'
        description = 'Updates gh cli'
        epilog = 'Usage: ghupdate download'
        arguments = [
            (['-v', '--version'],
             {'action': 'version',
              'version': VERSION_BANNER}),
        ]

    def _default(self):
        """Default action if no sub-command is passed."""

        self.app.args.print_help()
