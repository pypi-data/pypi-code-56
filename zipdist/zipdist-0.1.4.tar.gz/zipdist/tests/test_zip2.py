from zipdist.zip2 import Zipdist2
import pytest
import pandas as pd
import numpy as np
import sys
import os

def test_Zipdist2():
	class X():
		def __init__(self, name):
			self.name = name

	x = X(name = 'examplezip2')
	x.year = 2020
	x.exnp = np.zeros(3)
	x.expd = pd.DataFrame({"A":[1,2,3], "B":[2,4,6]})

	z = Zipdist2(name = "examplezip2", target = x)
	assert z.target is x


	z._save(dest = "xxx", dest_tar = "xxx.tar.gz")
	assert os.path.isfile("xxx.tar.gz")

	x2 = X(name = 'examplezip2')
	assert 'year' not in x2.__dict__.keys()
	z._build(target = x2, dest = "xxx", dest_tar = "xxx.tar.gz")
	print(x.__dict__.keys())
	assert isinstance(x2.exnp, np.ndarray)
	#assert np.all(x2.exnp == x.exnp)
	print(x2.exnp)
	print(x.exnp)
	assert np.array_equal(x2.exnp, x.exnp)
	assert np.all(x2.expd.equals(x.expd))
	assert np.all(x2.name == x.name)
	assert np.all(x2.year == x.year)


def test_Zipdist2_example():
	from zipdist.zip2 import Zipdist2
	import pandas as pd
	import numpy as np
	import os

	class X():
		def __init__(self, name):
			self.name = name

	x = X(name = 'example_target_object')
	x.example_simple_attr = [1989, 2020]
	x.example_np_attr = np.array([[0, 1, 2, 3], [4, 5, 6, 7]])
	x.example_pd_attr  = pd.DataFrame({"A":[1,2,3], "B":[2,4,6]})

	z = Zipdist2(name = "zipper", target = x)
	z._save(dest = "archive", dest_tar = "archive.tar.gz")
	assert os.path.isfile("archive.tar.gz")

	x_new = X(name = 'example_target_object')
	z = Zipdist2(name = "zipper", target = x_new)

	# You can use the z._build() and reload all object attributes
	z._build(target = x_new, dest = "archive", dest_tar = "archive.tar.gz")

	print(f"For instance:")
	print(f"\tx_new.example_simple_attr:\n{x_new.example_simple_attr}")
	print(f"\tx_new.example_np_attr:\n{x_new.example_np_attr}")
	print(f"\tx_new.example_pd_attr:\n{x_new.example_pd_attr}")

	# You can alternatively use the z._ready() and reload object attributes one by one
	x_new = X(name = 'example_target_object')
	z = Zipdist2(name = "zipper", target = x_new)
	z._ready(target = x_new, dest = "archive", dest_tar = "archive.tar.gz")
	z._reload_complex(k='example_np_attr')
	z._reload_simple(k='example_simple_attr')

"""
	Saving example_np_attr to .csv : archive/example_np_attr.csv
	Saving example_np_attr to .npy : archive/example_np_attr.npy
	Saving example_pd_attr to .csv : archive/example_pd_attr.csv
	Saving example_pd_attr to .feather : archive/example_pd_attr.feather
	Saving JSON with complex attribute definitions : archive/complex_attributes.json
	Saving JSON with simple attribute definitions : archive/simple_attributes.json
	Combining saved files in : [archive.tar.gz].
	Setting simple attribute name to example_target_object
	Setting simple attribute example_simple_attr to [1989, 2020]
	Setting [npy] to [np.ndarray] for attribute example_np_attr from: example_np_attr.npy
	Setting [feather] to [pd.DataFrame] for attribute example_pd_attr from: example_pd_attr.feather
For instance:
	x_new.example_simple_attr:
[1989, 2020]
	x_new.example_np_attr:
[[0 1 2 3]
 [4 5 6 7]]
	x_new.example_pd_attr:
   A  B
0  1  2
1  2  4
2  3  6
	You have not reloaded any object attributes yet, but you can from /archive/
	If you meant to auto-reload the object, Try ._build() instead of ._ready()
	Or for loading numpy and pandas attributes attributes one by one:
		try ._reload_complex(k = ATTRIBUTE_NAME)
"""



def test_cleanups():
	""" Adds cleanup of folders and .tar.gz files produced during testing"""
	os.system(f"rm -rf xxx")
	os.system(f"rm archive.tar.gz")
	os.system(f"rm xxx.tar.gz")