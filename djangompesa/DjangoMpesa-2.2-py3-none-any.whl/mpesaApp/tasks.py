from __future__ import absolute_import, unicode_literals
from celery import task
from celery.utils.log import get_task_logger

from mpesaApp.models import  mpesaDetail,payment,QueryURLS

import requests
from requests.auth import HTTPBasicAuth
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)



@task()
def comrfirm_payment_task():

	details = mpesaDetail.objects.all()

	api_url_query=QueryURLS.objects.get(id=1)

	for val in details:
		consumer_key = val.consumer_key

		consumer_secret = val.CONSUMER_SECRET

		token_api_URL = val.GENERATE_TOKEN_URL

		r = requests.get(token_api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))

		access_token = r.json()['access_token']

		print('access_token-->>>>> {0}'.format(access_token))

		api_url = str(val.api_url)
		headers = {"Authorization": "Bearer %s" % access_token}


		print(val)

	objects = payment.objects.filter(payment_status_message="")

	for obj in objects:

		api_url = api_url_query.api_url_query


		headers = {"Authorization": "Bearer %s" % access_token}
		request = { "BusinessShortCode": val.BusinessShortCode ,
		      "Password": val.Password,
		      "Timestamp": val.Timestamp,
		      "CheckoutRequestID": obj.CheckoutRequestID
		}

		response = requests.post(api_url, json = request, headers=headers)
		code = response.json()['ResultCode']
		message = response.json()['ResultDesc']
		if code=="0":
		    obj.success = True
		    obj.payment_status_message=message

		    obj.save()
		else:
		    obj.success = False
		    obj.payment_status_message=message
		    obj.save()


	return f"Objects-{objects}"