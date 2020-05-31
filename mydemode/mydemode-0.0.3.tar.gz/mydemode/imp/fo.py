from ..rest.epf import epf_rest


def lo():
	return epf_rest.get_epf()