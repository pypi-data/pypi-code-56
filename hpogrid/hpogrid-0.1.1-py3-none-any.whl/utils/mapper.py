import importlib

import hpogrid


def get_method(module, method):
	module = importlib.import_module(module)
	method = getattr(module, method)
	return method

search_space = {
	'hyperopt': get_method('hpogrid.search_space.hyperopt_space', 'HyperOptSpace'),
	'skopt': get_method('hpogrid.search_space.skopt_space', 'SkOptSpace'),
	'ax': get_method('hpogrid.search_space.ax_space', 'AxSpace'),
	'nevergrad': get_method('hpogrid.search_space.nevergrad_space', 'NeverGradSpace'),
	'bohb': get_method('hpogrid.search_space.bohb_space', 'BOHBSpace'),
	'tune': get_method('hpogrid.search_space.tune_space', 'TuneSpace')
}

algorithm = {
	'hyperopt': get_method('hpogrid.algorithm.hyperopt_algorithm', 'HyperOptAlgoWrapper'),
	'skopt': get_method('hpogrid.algorithm.skopt_algorithm', 'SkOptAlgoWrapper'),
	'ax': get_method('hpogrid.algorithm.ax_algorithm', 'AxAlgoWrapper'),
	'nevergrad': get_method('hpogrid.algorithm.nevergrad_algorithm', 'NeverGradAlgoWrapper'),
	'bohb': get_method('hpogrid.algorithm.bohb_algorithm', 'BOHBAlgoWrapper'),
}

generator = {
	'hyperopt': get_method('hpogrid.generator.hyperopt_generator', 'HyperOptGenerator'),
	'skopt': get_method('hpogrid.generator.skopt_generator', 'SkOptGenerator'),
	'ax': get_method('hpogrid.generator.ax_generator', 'AxGenerator'),
	'nevergrad': get_method('hpogrid.generator.nevergrad_generator', 'NeverGradGenerator'),
	'bohb': get_method('hpogrid.generator.bohb_generator', 'BOHBGenerator'),
}
