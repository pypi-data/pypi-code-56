import re
import subprocess
import sys
import traceback

import click
import click.core
import click.exceptions


_re_error_message_keywords = re.compile(
    r'^(error|aborted|failed|fatal)[:!]', flags=re.IGNORECASE | re.MULTILINE)


def _echo_stderr_red(message, *args, **kwargs):
    if sys.exc_info() and kwargs.get('file') is sys.stderr:
        # Only modify the message if an exception is currently being
        # handled and we're printing to STDERR.

        # Capitalize keywords in the error message
        message = _re_error_message_keywords.sub(
            lambda m: m.group(0).upper(), message)
        # Make it red
        message = click.style(message, fg='red')

    return click.echo(message, *args, **kwargs)


click.exceptions.echo = _echo_stderr_red
click.core.echo = _echo_stderr_red


class _UsageErrorWithFullHelp(click.exceptions.UsageError):
    def show(self, *args, **kwargs):
        # Swap out get_usage for get_help
        get_usage = self.ctx.get_usage
        self.ctx.get_usage = self.ctx.get_help
        try:
            return super().show(*args, **kwargs)
        finally:
            # Change it back
            self.ctx.get_usage = get_usage


click.exceptions.UsageError = _UsageErrorWithFullHelp
click.UsageError = _UsageErrorWithFullHelp


def _excepthook_red(etype, value, tb):
    # Print exception in red
    click.secho(
        ''.join(traceback.format_exception(etype, value, tb)),
        fg='red', file=sys.stderr, nl=False,
    )
    sys.exit(1)


sys.excepthook = _excepthook_red


def hecho(message, level=1):
    """Print a heading in a style inspired by Homebrew"""
    heading_colors = {
        1: 'green',
        2: 'blue',
        3: 'magenta',
    }
    arrow_color = heading_colors[level]
    click.echo(' '.join((
        click.style('==>', fg=arrow_color),
        click.style(message, bold=True),
    )))


def h1echo(msg):
    """Print a level 1 heading"""
    hecho(msg, level=1)


def h2echo(msg):
    """Print a level 2 heading"""
    hecho(msg, level=2)


def h3echo(msg):
    """Print a level 3 heading"""
    hecho(msg, level=3)


click.hecho = hecho
click.h1echo = h1echo
click.h2echo = h2echo
click.h3echo = h3echo


_subproc_run_default_hmsg = '$ {command}'


def subproc_run(
        args, hmsg=_subproc_run_default_hmsg, hlevel=1, fg=True, **kwargs):
    """User-friendly wrapper around subprocess.run"""
    check = kwargs.get('check', True)
    kwargs['check'] = False
    kwargs['shell'] = False

    if not fg:
        kwargs['capture_output'] = True
        if hmsg is _subproc_run_default_hmsg:
            hmsg = None

    command = ' '.join((f"'{a}'" if ' ' in a else a) for a in args)

    if hmsg:
        hecho(hmsg.format(command=command, args=args), level=hlevel)

    proc_result = subprocess.run(args, **kwargs)

    if check and proc_result.returncode != 0:
        error_message = (
            f'ERROR: Command "{command}" returned non-zero exit status '
            f'{proc_result.returncode}'
        )
        if proc_result.stderr:
            error_message += f'\nSTDERR:\n{proc_result.stderr}'
        click.secho(error_message, fg='red')
        sys.exit(1)

    return proc_result


click.subproc_run = subproc_run
