#!/usr/bin/env python

"""Tests for `carlae.cli` package."""
import carlae.cli
import pytest
from click.testing import CliRunner
from carlae.cli import cli


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(carlae.cli.cli)
    assert result.exit_code == 0
    assert "Usage: cli" in result.output
    help_result = runner.invoke(carlae.cli.cli, ["--help"])
    assert help_result.exit_code == 0
    assert "--log-level LVL" in help_result.output
