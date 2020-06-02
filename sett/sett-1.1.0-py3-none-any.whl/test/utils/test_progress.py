import unittest
from unittest import mock
import io

from sett.utils import progress


class TestProgress(unittest.TestCase):
    def test_scale_progress(self):
        self.assertEqual(progress.scale_progress(None, 0., 1,), None)
        p = progress.ProgressInterface()
        p.update = mock.Mock()
        sub_progress = progress.scale_progress(p, -1., 1.)
        sub_progress.update(0.)
        sub_progress.update(0.5)
        sub_progress.update(1.)
        p.update.assert_has_calls([mock.call(-1.),
                                   mock.call(0.), mock.call(1.)])

    @staticmethod
    def test_progress_iter():
        p = progress.ProgressInterface()
        p.update = mock.Mock()
        n = 3
        p_iter = progress.progress_iter(range(n), p)
        for _ in p_iter:
            pass
        p.update.assert_has_calls([mock.call(i / n) for i in range(n + 1)])

    def test_progress_iter_with_sub_progress(self):
        p = progress.ProgressInterface()
        p.update = mock.Mock()
        n = 3
        rng = (range(n),) * n

        for sub_rng, sub_progress in \
                progress.progress_iter_with_sub_progress(rng, p):
            for _ in progress.progress_iter(sub_rng, sub_progress):
                pass

        for call, pos in zip(p.update.call_args_list,
                             ((i + j / n) / n
                              for i in range(n) for j in range(n + 1))):
            (arg,), _ = call
            self.assertAlmostEqual(arg, pos)

    def test_subprogress(self):
        # Create a simple implementation of a progress interface.
        class SimpleProgressBar(progress.ProgressInterface):
            def __init__(self):
                self._completed_fraction = 0
                self._label = ''

            def update(self, completed_fraction: float) -> None:
                self._completed_fraction = completed_fraction

            def set_label(self, label: str) -> None:
                self._label = label

            def get_completed_fraction(self) -> float:
                return self._completed_fraction

        # Create a new instance of a simple progress bar.
        p = SimpleProgressBar()
        completion_values = (0, 0.1, 0.5, 0.7, 1)
        subprogress_step_values = (0.5, 0.3, 0.2)
        step_nb = 0

        # Loop through the 2 subprogress steps of the progress bar.
        for increase in subprogress_step_values:
            step_nb += 1
            # Compute start and stop points for the current subprogress bar.
            # We use these values to test that the subprogress bar returns
            # the correct values.
            start = sum(subprogress_step_values[:step_nb - 1])
            stop = start + increase

            # Initialize subprogress bar.
            with progress.subprogress(progress=p,
                                      step_completion_increase=increase,
                                      step_label=f'step {step_nb}') as subp:
                for x in completion_values:
                    subp.update(x)
                    # Verify the completed fraction of the global progress
                    # bar is correct.
                    expected = start + x * (stop - start)
                    self.assertEqual(p.get_completed_fraction(), expected,
                                     f'global fraction should be {expected}')
                    # Verify the completed fraction of the subprogress bar
                    # is correct. The completed fraction
                    self.assertAlmostEqual(subp.get_completed_fraction(), x,
                                           msg=f'subp fraction should be {x}')

        # Test the function when progress is None.
        p = None
        with progress.subprogress(progress=p, step_completion_increase=1,
                                  step_label='') as subp:
            pass

    def test_with_progress(self):
        p = progress.ProgressInterface()
        p.update = mock.Mock()
        for char, IoType in (('.', io.StringIO), (b'.', io.BytesIO)):
            with self.subTest(type=IoType):
                f = IoType(char * 10)
                f_progress = progress.with_progress(f, p)
                self.assertEqual(f_progress.read(3), char * 3)
                p.update.assert_called_once_with(3 / 10)
                p.update.reset_mock()
                self.assertEqual(f_progress.read(), char * 7)
                p.update.assert_called_once_with(1.)
                p.update.reset_mock()

        f = progress.with_progress(io.StringIO("1\n2\n3\n"), p)
        self.assertEqual(f.readlines(), ["1\n", "2\n", "3\n"])
        p.update.assert_called_once_with(1.)
        p.update.reset_mock()

        f = io.StringIO("1\n2\n3\n")
        for i, line in enumerate(progress.with_progress(f, p), 1):
            self.assertEqual(line, str(i) + '\n')
            p.update.assert_called_once_with(i / 3)
            p.update.reset_mock()
