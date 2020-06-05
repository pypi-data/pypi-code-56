import test_minimize_constrained

from ipopt import minimize_ipopt

test_minimize_constrained.minimize = minimize_ipopt

test = test_minimize_constrained.TestTrustRegionConstr()

test.test_default_jac_and_hess()

test.test_list_of_problems()
