from zipdist.zip import Zipdist
import pytest
import pandas as pd
import numpy as np
import sys
import os

""" Unit Tests """

def test_Zipdist_init():
	z = Zipdist(name = "testname")
	assert z.name == 'testname'

def test_Zipist_gets_attributes():
	class Y(Zipdist):
		def __init__(self):
			self.attr1 = 1

	y = Y()
	list_of_attr_keys = y._get_attributes()
		# returns as list
	assert isinstance(list_of_attr_keys, list)
		# attr1 is in list
	assert 'attr1' in list_of_attr_keys
		# only 'attr1` is in list
	assert y._get_attributes() == ['attr1']

def test_Zipist_gets_attribute_types():
	class Y(Zipdist):
		def __init__(self):
			self.attr1 = 1
			self.attr2 = '2'
			self.attr3 = {"A":"a"}
			self.attr4 = [1,3]
			self.attr5 = np.ndarray([1,3,4])

	y = Y()
	dict_of_attr_and_attr_types = y._get_attribute_types()
	assert isinstance(dict_of_attr_and_attr_types, dict)
	assert dict_of_attr_and_attr_types['attr1'] is int
	assert dict_of_attr_and_attr_types['attr2'] is str
	assert dict_of_attr_and_attr_types['attr3'] is dict
	assert dict_of_attr_and_attr_types['attr4'] is list
	assert dict_of_attr_and_attr_types['attr5'] == type(np.ndarray([1,3,4]))
	assert dict_of_attr_and_attr_types['attr5'] == np.ndarray

def test_Zipdist_ready(capsys):
	class Y(Zipdist):
		def __init__(self, name):
			self.name = name
	z = Y(name = "testname")
	z._save()
	assert(os.path.isfile('testname.tar.gz'))
	
	z2 = Y('testname')
	z2._ready()


def test_Zipdist_read():
	z = Zipdist(name = "testonly")
	z._make_dest_directory("blah")
	assert os.path.isdir("blah")


def test_Zipdist_with_deeper_path():
	""" 
	Supposing that we want to store .tag.gz in a deeper folder ./layer1
	instead of working dir. 
	"""
	if not os.path.isdir('layer1'):
		os.mkdir("layer1")
	class Y(Zipdist):
		def __init__(self, name):
			self.name = name
			self.year = None

	y = Y('Flanders')
	y.years = [2020,2019]
	y.bart = np.zeros(10)
	y.lisa = pd.DataFrame([{"Pi":3.1415,"e":2.7182}])
	y._save(dest = "layer1/Flanders", dest_tar = "layer1/Flanders.tar.gz" )
	assert os.path.isfile("layer1/Flanders.tar.gz")

	 # Create a New Object, None of the prior attributes exists
	y2 = Y("Flanders")
	assert 'bart' not in y2.__dict__.keys()
	assert 'years' not in y2.__dict__.keys()
	# But you can rebuilt it
	y2._build(dest="layer1/Flanders", dest_tar = "layer1/Flanders.tar.gz")
	assert isinstance(y2.bart, np.ndarray)
	assert isinstance(y2.lisa, pd.DataFrame)


def test_Zipdist_with_shallower_path():
	""" 
	Supposing that we want to store .tag.gz in a deeper folder ./layer1
	instead of working dir. 
	"""
	class Y(Zipdist):
		def __init__(self, name):
			self.name = name
			self.year = None

	y = Y('Flanders')
	y.years = [2020,2019]
	y.bart = np.zeros(10)
	y.lisa = pd.DataFrame([{"Pi":3.1415,"e":2.7182}])
	y._save(dest = "../Springfield", dest_tar = "../Springfield.tar.gz" )
	assert os.path.isfile("layer1/Flanders.tar.gz")

	 # Create a New Object, None of the prior attributes exists
	y2 = Y("Flanders")
	assert 'bart' not in y2.__dict__.keys()
	assert 'years' not in y2.__dict__.keys()
	# But you can rebuilt it
	y2._build(dest = "../Springfield", dest_tar = "../Springfield.tar.gz")
	assert isinstance(y2.bart, np.ndarray)
	assert isinstance(y2.lisa, pd.DataFrame)




""" Integration Tests """
def test_basic_example():
	""" Do a full _save and _build basic example """
	class Y(Zipdist):
		def __init__(self, name):
			self.name = name
			self.year = None

	y = Y(name ='Simpsons')
	y.years = [1989, 2020]
	y.bart = np.zeros(10)
	y.lisa = pd.DataFrame([{"Pi":3.1415,"e":2.7182}])
	y._save(dest="Simpsons", dest_tar = "Simpsons.tar.gz")


	ynew = Y(name = "Simpsons")
	ynew._build(dest="Simpsons", dest_tar = "Simpsons.tar.gz")
	sys.stdout.write(f"ynew.years: {ynew.years}\n")
	sys.stdout.write(f"ynew.lisa:\n{ynew.lisa}\n")
	sys.stdout.write(f"ynew.bart: {ynew.bart}\n")
	ynew = Y("Simpsons")
	assert 'lisa' not in ynew.__dict__.keys()
	assert 'bart' not in ynew.__dict__.keys()
	assert 'years' not in ynew.__dict__.keys()
	ynew._ready(dest="Simpsons", dest_tar = "Simpsons.tar.gz")
	ynew._reload_complex('lisa')
	assert isinstance(ynew.lisa, pd.DataFrame)
	ynew._reload_simple('years')
	assert isinstance(ynew.years, list)


def test_Zipdist_save_using_name_attribute_only():
	""" 
	What about case were user does not specify dest and dest directly
		As long as they provide a name, name/ nad name.tar.gz, 
		should serve as the repositories.
	"""
	class Y(Zipdist):
		def __init__(self, name):
			self.name = name

	y = Y(name = 'siblings')
	y.bart = np.zeros(10)
	y.lisa = pd.DataFrame([{"Pi":3.1415,"e":2.7182}])
	y._save()
	assert os.path.isfile("siblings.tar.gz")

def test_Zipdist_build_using_name_attribute_only():
	""" 
	What about case were user does not specify dest and dest directly
		As long as they provide name matchign the name.tar.gz, test
		that _build should work.
	"""
	class Y(Zipdist):
		def __init__(self, name):
			self.name = name

	y = Y(name = 'siblings')
	y.bart = np.zeros(10)
	y.lisa = pd.DataFrame([{"Pi":3.1415,"e":2.7182}])
	y._save()
	assert os.path.isfile("siblings.tar.gz")

	y2 = Y(name = 'siblings')
	y2._build()
	assert isinstance(y2.bart, np.ndarray)
	assert isinstance(y2.lisa, pd.DataFrame)

def test_Zipdist_reload_complex():
	""" Example Where only one attribute is loaded using _ready, _reload_complex"""
	class Y(Zipdist):
		def __init__(self, name):
			self.name = name

	y = Y(name = 'Simpsons')
	y.bart = np.zeros(10)
	y.lisa = pd.DataFrame([{"Pi":3.1415,"e":2.7182}])
	y._save(dest="Simpsons", dest_tar = "Simpsons.tar.gz")
	y2 = Y('Simpsons')
	with pytest.raises(AttributeError):
		y2.lisa
	y2._ready()
	print(y2._complex_attributes)
	y2._reload_complex(k ='lisa')
	assert isinstance(y2.lisa, pd.DataFrame)

def test_Zipdist_reload_simple():
	""" Example Where only one attribute is loaded using _ready, _reload_complex"""
	class Y(Zipdist):
		def __init__(self, name):
			self.name = name

	y = Y(name = 'Simpsons')
	y.homer = 1
	y.bart = np.zeros(10)
	y.lisa = pd.DataFrame([{"Pi":3.1415,"e":2.7182}])
	y._save(dest="Simpsons", dest_tar = "Simpsons.tar.gz")

	y2 = Y('Simpsons')
	with pytest.raises(AttributeError):
		y2.lisa
	y2._ready()
	y2._reload_simple(k = "homer")
	assert y2.homer == 1


def test_Zipdist_reload_complex_KeyError():
	""" Example Where only one attribute is loaded using _ready, _reload_complex"""
	class Y(Zipdist):
		def __init__(self, name):
			self.name = name

	y = Y(name = 'Simpsons')
	y.homer = 1
	y.bart = np.zeros(10)
	y.lisa = pd.DataFrame([{"Pi":3.1415,"e":2.7182}])
	y._save(dest="Simpsons", dest_tar = "Simpsons.tar.gz")

	y2 = Y('Simpsons')
	with pytest.raises(AttributeError):
		y2.lisa
	y2._ready()
	with pytest.raises(KeyError):
		y2._reload_complex(k = "moe")

def test_Zipdist_reload_simple_KeyError():
	""" Example Where only one attribute is loaded using _ready, _reload_complex"""
	class Y(Zipdist):
		def __init__(self, name):
			self.name = name

	y = Y(name = 'Simpsons')
	y.homer = 1
	y.bart = np.zeros(10)
	y.lisa = pd.DataFrame([{"Pi":3.1415,"e":2.7182}])
	y._save(dest="Simpsons", dest_tar = "Simpsons.tar.gz")

	y2 = Y('Simpsons')
	with pytest.raises(AttributeError):
		y2.lisa
	y2._ready()
	y2._reload_simple(k = "homer")
	assert y2.homer == 1
	with pytest.raises(KeyError):
		y2._reload_complex(k = "marge")

def test_Zipdist_reload_simple_warning_for_missing():
	""" Example Where only one attribute is loaded using _ready, _reload_complex"""
	class Y(Zipdist):
		def __init__(self, name):
			self.name = name

	y = Y(name = 'Simpsons')
	y.homer = 1
	y.bart = np.zeros(10)
	y.lisa = pd.DataFrame([{"Pi":3.1415,"e":2.7182}])
	y._save(dest="Simpsons", dest_tar = "Simpsons.tar.gz")

	y2 = Y('Simpsons')
	with pytest.raises(AttributeError):
		y2.lisa
	y2._ready()
	y2._reload_simple(k = "homer")
	assert y2.homer == 1
	with pytest.warns(UserWarning) as w:
		y2._reload_simple(k = "maggie")
		assert len(w) == 1
		assert w[0].message.args[0] == "Could not reload simple attribute maggie"


def test_cleanups():
	""" Adds cleanup of folders and .tar.gz files produced during testing"""
	os.system(f"rm -rf Simpsons")
	os.system(f"rm -rf siblings")
	os.system(f"rm -rf testname")
	os.system(f"rm -rf blah")
	os.system(f"rm -rf layer1")
	os.system(f"rm -rf Flanders")
	os.system(f"rm -rf Springfield")
	os.system(f"rm Simpsons.tar.gz")
	os.system(f"rm testname.tar.gz")
	os.system(f"rm siblings.tar.gz")










