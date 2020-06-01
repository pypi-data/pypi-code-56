from .utils import generate_oauth_url, generate_xml, validate_params


class Pesapal():
	r"""
	This is a more generic way of integrating a Python application with PesaPal.
	It also serves as the base class of `PesapalFlask` that is included in this package.
	"""
	
	def __init__(self, consumer_key, consumer_secret, testing = True, prettyprint_xml = True, save_xml_file = False, xml_output_dir = None, param_validation = True):
		r"""
		:param consumer_key: The consumer key (sometimes referred to as client key) provided by PesaPal.
		:param consumer_secret: The consumer secret (sometimes referred to as client secret) provided by PesaPal.
		:param testing: (Optional) A Boolean that sets the PesaPal URL to either the testing environment (https://demo.pesapal.com) or the production environment (https://pesapal.com). Default value is `True`.
		:param prettyprint_xml: (Optional) A Boolean that sets whether the generated XML is to be prettyprinted or not. Default value is `True`.
		:param save_xml_file: (Optional) A Boolean that sets whether an XML file should be written to disk or not. Default value is `False`.
		:param xml_output_dir: (Optional) A string that defines where XML files shall be saved. Defaults to the `xml` directory in the current working directory.
		"""
		self.consumer_key = str(consumer_key)
		self.consumer_secret = str(consumer_secret)
		self.testing = testing
		self.prettyprint_xml = prettyprint_xml
		self.save_xml_file = save_xml_file
		self.xml_output_dir = xml_output_dir
		self.param_validation = param_validation

		if self.testing:
			self.base_url = "https://demo.pesapal.com/{}"
		else:
			self.base_url = "https://pesapal.com/{}"


	def post_order(self, callback_url = None, transaction_data = None):
		r"""
		Use this to generate the URL used to post a transaction to PesaPal.
		------------------------------------------------------------------

		:param callback_url: This is the URL that a user will be redirected to once the payment process has been completed.
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
		
		xml_defaults = {
			"amount": True,
			"description": True,
			"type": False,
			"reference": True,
			"email": True,
			"phone_number": False,
			"currency": True,
			"first_name": False,
			"last_name": False,
			"line_items": False
		}

		if self.param_validation:
			validate_params(transaction_data, xml_defaults)
		
		xml_data = generate_xml(transaction_data, prettyprint = self.prettyprint_xml, generate_xml_file = self.save_xml_file, xml_output_directory = self.xml_output_dir)
		pesapal_url = self.base_url.format("api/PostPesapalDirectOrderV4")

		params = {
			"oauth_callback": callback_url,
			"pesapal_request_data": xml_data
		}

		url = generate_oauth_url(self.consumer_key, self.consumer_secret, pesapal_url, params)

		return url


	def query_payment_status(self, merchant_ref, pesapal_tracking_id):
		r"""
		Use this to generate the URL used to query the status of the transaction.
		------------------------------------------------------------------------

		:param merchant_ref: The transaction ID (or 'reference') sent to PesaPal when posting the transaction.
		:param pesapal_tracking_id: The ID returned by PesaPal as the query parameter 'pesapal_transaction_tracking_id'.
		:return: The generated URL.
		:rtype: string
		"""

		pesapal_url = self.base_url.format("api/QueryPaymentStatus")
		
		params = {
			"pesapal_merchant_reference": merchant_ref,
			"pesapal_transaction_tracking_id": pesapal_tracking_id
		}

		url = generate_oauth_url(self.consumer_key, self.consumer_secret, pesapal_url, params)

		return url


	def query_payment_status_by_merchant_ref(self, merchant_ref):
		r"""
		Use this to generate the URL used to query the payment status with just the transaction ID
		------------------------------------------------------------------------------------------

		:param merchant_ref: The transaction ID (or 'reference') sent to PesaPal when posting the transaction.
		:return: The generated URL.
		:rtype: string
		"""

		pesapal_url = self.base_url.format("api/QueryPaymentStatusByMerchantRef")

		params = {
			"pesapal_merchant_reference": merchant_ref
		}

		url = generate_oauth_url(self.consumer_key, self.consumer_secret, pesapal_url, params)

		return url


	def query_payment_details(self, merchant_ref, pesapal_tracking_id):
		r"""
		Use this to generate the URL used to query the details of the transaction
		-------------------------------------------------------------------------
		
		:param merchant_ref: The transaction ID (or 'reference') sent to PesaPal when posting the transaction.
		:param pesapal_tracking_id: The ID returned by PesaPal as the query parameter 'pesapal_transaction_tracking_id'.
		:return: The generated URL.
		:rtype: string
		"""

		pesapal_url = self.base_url.format("api/QueryPaymentDetails")
		
		params = {
			"pesapal_merchant_reference": merchant_ref,
			"pesapal_transaction_tracking_id": pesapal_tracking_id
		}

		url = generate_oauth_url(self.consumer_key, self.consumer_secret, pesapal_url, params)

		return url


	def generate_iframe(self, callback_url = None, transaction_data = None, attr = None):
		r"""
		Use this to generate HTML code for the iframe that can be used as an alternative to the API calls
		-------------------------------------------------------------------------------------------------

		:param callback_url: This is the URL that a user will be redirected to once the payment process has been completed.
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

		url = self.post_order(callback_url, transaction_data)

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