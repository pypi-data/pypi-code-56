from skopt import Optimizer

import ray
from ray.tune.suggest.skopt import SkOptSearch

from hpogrid.search_space.skopt_space import SkOptSpace



class SkOptAlgoWrapper():
	def __init__(self):
		self.algorithm = None
	def create(self, metric, mode, search_space, **args):
		search_space = SkOptSpace(search_space).search_space
		optimizer = Optimizer(search_space)
		hp_names = []
		for hp in search_space:
			hp_names.append(hp.name)

		self.algorithm = SkOptSearch(optimizer, hp_names, metric=metric, mode=mode, **args)
		return self.algorithm