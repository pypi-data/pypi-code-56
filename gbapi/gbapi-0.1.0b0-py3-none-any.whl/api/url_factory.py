__all__ = ['URLFactory']

class URLFactory:
	def __init__(self, base_url):
		if not isinstance(base_url, str):
			raise TypeError(
				"from URLFactory: "
				f"base_url must be `str`, not `{type(base_url)}`!"
			)
		self.base_url = base_url

	def make(self, url, module):
		return f"{self.base_url}/{url}?api={module}"