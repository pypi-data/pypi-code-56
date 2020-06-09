import click


# Monkeypatch click BaseCommand help options.
# Cf. https://github.com/pallets/click/issues/646#issuecomment-389969474

orig_basecommand_init = click.core.BaseCommand.__init__

def new_basecommand_init(self, *args, **kwargs):
    orig_basecommand_init(self, *args, **kwargs)
    self.context_settings['help_option_names'] = ['--help', '-h']

click.core.BaseCommand.__init__ = new_basecommand_init
