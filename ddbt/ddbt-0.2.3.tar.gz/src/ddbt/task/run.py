import inspect
import json
from typing import Dict, Optional

import attr
import dbt.main as dbt
import dbt.task.run as run_task
from dbt.exceptions import RuntimeException
from dbt.logger import GLOBAL_LOGGER as logger
from dbt.logger import log_manager
from dbt.ui.printer import green, red

from ddbt.constants import START_MESSAGE
from ddbt.exceptions import NoModelsFoundException
from ddbt.task.base import GitTask, TimeRangeTask


@attr.s(auto_attribs=True)
class RunTask(TimeRangeTask, GitTask):
    @classmethod
    def from_args(cls, args):
        return cls(
            start=args.start,
            end=args.end,
            granularity=args.granularity,
            increment=args.increment,
            cached_changes=args.cached_changes,
            last_changes=args.last_changes,
            commit_diff=args.commit_diff,
            commit_id=args.commit_id,
            materialization=args.materialization,
            models=args.models,
            exclude=args.exclude,
            args=args,
        )

    def _set_vars(
        self, time_interval: Dict[str, str], input_vars: Optional[Dict[str, str]]
    ):
        """Set variables

        Args:
            time_interval (Dict[str, str]): Time interval variables
            input_vars (Optional[Dict[str, str]]): Input variables
        """
        if input_vars:
            time_interval.update(input_vars)
        self.args.vars = json.dumps(time_interval)

    def run(self):
        self._load_manifest()
        # Set models to selected models and cls back to dbt RunTask
        try:
            self.args.models = self._update_models()
            self.args.cls = run_task.RunTask
            input_vars = json.loads(self.args.vars)

            time_range = self.time_range()
            msg_tmp = inspect.cleandoc(START_MESSAGE)
            exec_results = []
            for time_interval in time_range:
                self._set_vars(time_interval, input_vars)
                msg = msg_tmp.format(
                    i=self.processed + 1,
                    iter_no=len(time_range),
                    start=self.start,
                    end=self.end,
                    granularity=self.granularity,
                    increment=self.increment,
                    start_timestamp=time_interval.get("start_timestamp"),
                    next_timestamp=time_interval.get("next_timestamp"),
                )
                logger.info(green(msg))
                task, res = dbt.run_from_args(self.args)
                exec_results.append(res)
                # True if success
                res_interpret = task.interpret_results(res)
                # invert result
                self.errors += int(not res_interpret)
                log_manager.reset_handlers()
                self.processed += 1

            if self.errors > 0:
                logger.info("\n")
                raise RuntimeException(
                    red(f"Some runs[{self.errors}] failed. " f"Please, check them!")
                )
        except NoModelsFoundException as e:
            exec_results = None
            logger.error(e)

        return exec_results, True
