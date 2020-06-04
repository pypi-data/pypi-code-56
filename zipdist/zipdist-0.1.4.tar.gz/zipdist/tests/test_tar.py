

# def test_create_tar():
# 	from zipdist.zip import Zipdist
# 	import pandas as pd
# 	import numpy as np
# 	import sys
# 	import os

# 	class Y(Zipdist):
# 		def __init__(self, name):
# 			self.name = name
# 			self.year = None

# 	y = Y(name ='Simpsons')
# 	y.years = [1989, 2020]
# 	y.bart = np.zeros(10)
# 	y.lisa = pd.DataFrame([{"Pi":3.1415,"e":2.7182}])
# 	y._save(dest="Simpsons", dest_tar = "Simpsons.tar.gz")
# 	assert os.path.isfile('Simpsons.tar.gz')


# # import tarfile

# # import os
# # import tarfile

# def _get_tarinfo_for_a_file(members, filename):
#     for tarinfo in members:
#     	print(tarinfo.name)
#     	if tarinfo.name == filename:
#     		print(tarinfo.name)
#     		yield tarinfo

# # tar = tarfile.open('Simpsons.tar.gz')
# # tar.extractall(members=_get_tarinfo_for_a_file(tar, filename = "Simpsons/lisa.csv"))
# # tar.close()


# with tempfile.TemporaryFile(suffix='.tar.gz') as f:
#     with tarfile.open(fileobj=f, mode='r:gz') as tar:
#     	# extract just one
#     	tar.extractall(members=_get_tarinfo_for_a_file(tar, filename = "Simpsons/lisa.csv"))


# tar = tarfile.open('Simpsons.tar.gz')
# fh = tar.extractfile('Simpsons/lisa.feather')

