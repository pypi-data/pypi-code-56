import os
import requests

from datetime import datetime
from requests_oauthlib import OAuth1
from xml.etree.ElementTree import Element, ElementTree, SubElement, Comment, tostring
from xml.dom import minidom


def prettyprint_xml(element):
	r"""
	Use this to return prettyprinted XML.
	------------------------------------

	:param element: An `ElementTree` Element.
	:return: UTF-8 decoded, prettyprinted XML.
	:rtype: string
	"""
	
	rough_string = tostring(element, "utf-8")
	reparsed = minidom.parseString(rough_string)
	return reparsed.toprettyxml(indent = "  ")


def generate_xml(transaction_data, prettyprint = True, generate_xml_file = False, xml_output_directory = None):
	r"""
	Use this to generate PesaPal-compliant XML documents.
	----------------------------------------------------

	:param transaction_data: A dict containing the transaction data.
	:param prettyprint: (Optional) A Boolean that sets whether the resultant XML output should be prettyprinted.
	:param generate_xml_file: (Optional) Set whether the function should generate an XML file. Defaults to `False`.
	:param xml_output_directory: (Optional) This defines where XML files shall be saved.
	:return: Generated XML.
	"""
	
	# Creating the parent element of the XML document
	xml_string = Element("PesapalDirectOrderInfo", {
		"xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
		"xmlns:xsd": "http://www.w3.org/2001/XMLSchema",
		"xmlns": "http://www.pesapal.com",
		"Amount": "{0:.2f}".format(transaction_data.get("amount", "0.00")),
		"Description": transaction_data.get("description", "Transaction description"),
		"Type": transaction_data.get("type", "MERCHANT"),
		"Reference": transaction_data.get("reference"),
		"FirstName": transaction_data.get("first_name", ""),
		"LastName": transaction_data.get("last_name", ""),
		"Email": transaction_data.get("email", ""),
		"PhoneNumber": transaction_data.get("phone", "")
	})

	if transaction_data.get("currency"):
		xml_string.set("currency", transaction_data.get("currency"))

	if len(transaction_data.get("line_items")) > 0:
		line_item_parent = SubElement(xml_string, "lineitems")

		for item in transaction_data.get("line_items"):
			line_item = SubElement(line_item_parent, "lineitem", {
				"UniqueId": str(item.get("item_id")),
				"Particulars": item.get("item_name"),
				"Quantity": str(item.get("item_count")),
				"UnitCost": "{0:.2f}".format(item.get("unit_cost")),
				"SubTotal": "{0:.2f}".format(item.get("subtotal"))
			}).text = ""

	if generate_xml_file:
		to_save = xml_string
		dir_to_save_to = "{}/xml".format(os.getcwd()) if not xml_output_directory else xml_output_directory
		filename = "{}_{}.xml".format(datetime.now().strftime("%Y-%m-%d"), transaction_data.get("reference"))

		try:
			ElementTree(to_save).write("{}/{}".format(dir_to_save_to, filename), "utf-8")
		except FileNotFoundError:
			os.makedirs(dir_to_save_to)
			ElementTree(to_save).write("{}/{}".format(dir_to_save_to, filename), "utf-8")
		except PermissionError:
			raise PermissionError("Unable to write the XML data to file.")
	
	if prettyprint:
		return prettyprint_xml(xml_string)
	else:
		return tostring(xml_string, "utf-8")


def generate_oauth_url(consumer_key, consumer_secret, url, request_params):
	r"""
	Use this to generate an OAuth1 URL.
	---------------------------------

	:param consumer_key: The consumer key (also called client key) provided by the service provider.
	:param consumer_secret: The consumer secret (also called client secret) provided by the service provider.
	:param url: The base URL, such as http://example.com
	:param request_params: A dict containing any other request parameters (or arguments) apart from what is generated as part of the OAuth request.
	:return: The generated URL string.
	"""
	
	oauth_signature = OAuth1(consumer_key, consumer_secret, signature_type = "query")

	_url = requests.Request("GET", url, params = request_params, auth = oauth_signature)
	url = _url.prepare()
	return url.url


def validate_params(params, required_params):
	r"""
	Use this to validate parameters passed against a dict of required params.
	------------------------------------------------------------------------

	:param params: The dict to be validated.
	:param required_params: A dict containing the keys to validate together with their required status as a Boolean.
		
		Example:
		{
			"key1": True,
			"key2": True,
			"key3": False
		}
	:return: `KeyError` if a required key is missing
	"""
	
	for key, value in list(required_params.items()):
		if value:
			# If the value is set to True, the key is required in the params passed
			if key not in params:
				error = "Required key '{}' not found in {}".format(key, list(params.keys()))
				raise KeyError(error)