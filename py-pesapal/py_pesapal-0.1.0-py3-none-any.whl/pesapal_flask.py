from .pesapal import Pesapal


class PesapalFlask(Pesapal):
	r"""
	Integrate a Flask application with PesaPal
	"""


	def __init__(self, app, config = None):
		r"""
		:param app: This is the Flask application instance
		:param config: (Optional) A dict that contains configuration values. If it is not set, configuration values are set based on the app's set configuration.
		"""

		if app is None:
			raise ValueError("'app' instance not set")

		if not config:
			configuration = app.config
		else:
			configuration = config

		self.consumer_key = configuration.get("PESAPAL_CONSUMER_KEY")
		self.consumer_secret = configuration.get("PESAPAL_CONSUMER_SECRET")
		self.testing = configuration.get("PESAPAL_TESTING", True)
		self.callback_url = configuration.get("PESAPAL_CALLBACK_URL")
		self.prettyprint_xml = configuration.get("PESAPAL_PRETTYPRINT_XML", True)
		self.save_xml_file = configuration.get("PESAPAL_SAVE_XML", False)
		self.xml_output_dir = configuration.get("PESAPAL_OUTPUT_DIR", None)
		self.param_validation = configuration.get("PESAPAL_PARAM_VALIDATION", True)

		if self.testing:
			self.base_url = "https://demo.pesapal.com/{}"
		else:
			self.base_url = "https://pesapal.com/{}"

		@app.context_processor
		def add_context_processors():
			r"""
			This is used to add context processors to the Flask application instance
			"""
			return dict(render_iframe = self.render_iframe)


	def post_order(self, transaction_data = None):
		r"""
		Use this to generate the URL used to post a transaction to PesaPal.
		------------------------------------------------------------------

		:param transaction_data: A dict containing all the details of the transaction.
			
			For example:
			{
				"amount": 100,
				"description": "Test description",
				"type": "MERCHANT", # Can be left blank
				"reference": "uuid",
				"email": "mail@example.com", # Unlike PesaPal's requirements, this needs to have a value
				"phone_number": "", # Can be left blank
				"currency": "KES",
				"first_name": "", # Can be left blank
				"last_name": "", # Can be left blank
				"line_items": [{
					"item_id": "1",
					"item_name": "Product 1",
					"item_count": 2,
					"unit_cost": 1,
					"subtotal": 2
				}]
			}
		:return: The generated URL.
		:rtype: string
		"""
		
		return super().post_order(callback_url = self.callback_url, transaction_data = transaction_data)


	def query_payment_status(self, merchant_ref, pesapal_tracking_id):
		r"""
		Use this to generate the URL used to query the status of the transaction.
		------------------------------------------------------------------------

		:param merchant_ref: The transaction ID (or 'reference') sent to PesaPal when posting the transaction.
		:param pesapal_tracking_id: The ID returned by PesaPal as the query parameter 'pesapal_transaction_tracking_id'.
		:return: The generated URL.
		:rtype: string
		"""

		return super().query_payment_status(merchant_ref, pesapal_tracking_id)


	def query_payment_status_by_merchant_ref(self, merchant_ref):
		r"""
		Use this to generate the URL used to query the payment status with just the transaction ID
		------------------------------------------------------------------------------------------

		:param merchant_ref: The transaction ID (or 'reference') sent to PesaPal when posting the transaction.
		:return: The generated URL.
		:rtype: string
		"""
		
		return super().query_payment_status_by_merchant_ref(merchant_ref)


	def query_payment_details(self, merchant_ref, pesapal_tracking_id):
		r"""
		Use this to generate the URL used to query the details of the transaction
		-------------------------------------------------------------------------
		
		:param merchant_ref: The transaction ID (or 'reference') sent to PesaPal when posting the transaction.
		:param pesapal_tracking_id: The ID returned by PesaPal as the query parameter 'pesapal_transaction_tracking_id'.
		:return: The generated URL.
		:rtype: string
		"""

		return super().query_payment_details(merchant_ref, pesapal_tracking_id)


	def generate_iframe(self, transaction_data = None, attr = None):
		r"""
		Use this to generate HTML code for the iframe that can be used as an alternative to the API calls
		-------------------------------------------------------------------------------------------------

		:param transaction_data: A dict containing all the details of the transaction.
			
			For example:
			{
				"amount": 100,
				"description": "Test description",
				"type": "MERCHANT", # Can be left blank
				"reference": "uuid",
				"email": "mail@example.com", # Unlike PesaPal's requirements, this needs to have a value
				"phone_number": "", # Can be left blank
				"currency": "KES",
				"first_name": "", # Can be left blank
				"last_name": "", # Can be left blank
				"line_items": [{
					"item_id": "1",
					"item_name": "Product 1",
					"item_count": 2,
					"unit_cost": 1,
					"subtotal": 2
				}]
			}
		:param attr: (Optional) A dict containing some basic attributes that can be used to change the default appearance of the iframe.

			Default values are:
			{
				"width": "100%",
				"height": "100%",
				"scrolling": "auto",
				"frameBorder": "0"
			}
		:return: HTML iframe snippet
		:rtype: string
		"""

		# Overriding the default implementation due to the difference in post_order methods
		url = self.post_order(transaction_data)

		style = {
			"width": "100%",
			"height": "100%",
			"scrolling": "auto",
			"frameBorder": "0"
		}

		if attr:
			style.update(attr)

		attr_string = ""
		for key, val in style.items():
			attr_string += "{}={} ".format(key, val)
		
		iframe = """
		<iframe src = "{}" {}>
		</iframe>
		""".format(url, attr_string)

		return iframe


	def render_iframe(self, transaction_data, attr = None):
		r"""
		Use this to render the PesaPal iframe within a Jinja2 template
		---------------------------------------------------------------
		
		:param transaction_data: A dict containing all the details of the transaction.
			
			For example:
			{
				"amount": 100,
				"description": "Test description",
				"type": "MERCHANT", # Can be left blank
				"reference": "uuid",
				"email": "mail@example.com", # Unlike PesaPal's requirements, this needs to have a value
				"phone_number": "", # Can be left blank
				"currency": "KES",
				"first_name": "", # Can be left blank
				"last_name": "", # Can be left blank
				"line_items": [{
					"item_id": "1",
					"item_name": "Product 1",
					"item_count": 2,
					"unit_cost": 1,
					"subtotal": 2
				}]
			}
		:param attr: (Optional) A dict containing some basic attributes that can be used to change the default appearance of the iframe.

			Default values are:
			{
				"width": "100%",
				"height": "100%",
				"scrolling": "auto",
				"frameBorder": "0"
			}
		:return: HTML iframe snippet
		:rtype: string
		"""

		iframe = self.generate_iframe(transaction_data, attr)

		return iframe