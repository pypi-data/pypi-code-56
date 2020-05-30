# -*- coding: utf-8 -*-

from datetime import datetime

import click

from slow_start_rewatch.config import Config
from slow_start_rewatch.scheduler import Scheduler
from slow_start_rewatch.timer import Timer


class App(object):
    """The main application object."""

    def __init__(self, config: Config) -> None:
        """Initialize App."""
        self.config = config
        self.timer = Timer(config)
        self.scheduler = Scheduler(config)

    def run(self) -> None:
        """Runs the application."""
        self.prepare()
        self.start()

    def prepare(self) -> None:
        """
        Make the preparations for the main run.

        - Load the scheduled Post.
        """
        self.scheduler.load(self.config["username"])

    def start(self) -> None:
        """
        Start the main run.

        1. Wait until the scheduled time.

        2. Proceed with the Post submission.
        """
        post = self.scheduler.scheduled_post

        if post is None:
            raise RuntimeError(
                "Cannot start the countdown without the scheduled post.",
            )

        self.timer.wait(post.submit_at)

        click.echo("{0}: A post to be submitted: {1} - {2}".format(
            datetime.now(),
            post.subreddit,
            post.title,
        ))
