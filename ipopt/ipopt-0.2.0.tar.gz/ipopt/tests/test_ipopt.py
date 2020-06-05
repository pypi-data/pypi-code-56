from .. import Problem, problem


def test_add_option():


    class Callbacks():

        def objective(self, x):
            return 1.0

        def gradient(self, x):
            return [1.0, 1.0]

    p = Problem(2, 4, problem_obj=Callbacks, cu=[5.0, 5.0, 5.0, 5.0])
    p.add_option('tol', 1e-7)
    p.addOption('mu_strategy', 'adaptive')

    p = Problem(2, 4, problem_obj=Callbacks, cu=[5.0, 5.0, 5.0, 5.0])
    p.add_option(b'tol', 1e-7)
    p.addOption(b'mu_strategy', b'adaptive')

    p = problem(2, 4, problem_obj=Callbacks, cu=[5.0, 5.0, 5.0, 5.0])
    p.add_option('tol', 1e-7)
    p.addOption('mu_strategy', 'adaptive')
