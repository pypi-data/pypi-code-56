# coding=u8
import logging
from KE import KE
import csv
from datetime import datetime, timedelta

client3 = KE(host='device2', username='admin', password='Kyligence@2020', version=3, debug=True)
client = KE(host=['10.1.3.63'], port=7171, username='ADMIN', password='KYLIN', version=4, debug=True)

p = client3.projects('learn_kylin')


