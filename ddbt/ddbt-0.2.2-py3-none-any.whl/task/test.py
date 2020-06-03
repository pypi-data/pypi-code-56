import attr
import dbt.main as dbt
import dbt.task.test as test_task
from dbt.exceptions import RuntimeException
from dbt.logger import GLOBAL_LOGGER as logger
from dbt.logger import log_manager
from dbt.ui.printer import red

from ddbt.exceptions import NoModelsFoundException
from ddbt.task.base import GitTask


@attr.s(auto_attribs=True)
class TestTask(GitTask):
    @classmethod
    def from_args(cls, args):
        return cls(
            cached_changes=args.cached_changes,
            last_changes=args.last_changes,
            commit_diff=args.commit_diff,
            commit_id=args.commit_id,
            materialization=args.materialization,
            models=args.models,
            exclude=args.exclude,
            args=args,
        )

    def run(self):
        self._load_manifest()
        # Set models to selected models and cls back to dbt RunTask
        try:
            self.args.models = self._update_models()
            self.args.cls = test_task.TestTask

            task, res = dbt.run_from_args(self.args)
            exec_results = []
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
                    red(f"Some tests[{self.errors}] failed. " f"Please, check them!")
                )
        except NoModelsFoundException as e:
            exec_results = None
            logger.error(e)

        return exec_results, True
