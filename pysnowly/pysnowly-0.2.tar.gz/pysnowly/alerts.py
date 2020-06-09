import json
import requests
import time
import random
import snowflake.connector

END_POINT_URL = 'https://api.snowly.io/v1'

WAIT_A_SEC = random.randint(0, 50)


def run(token='', accounts=[]):


    time.sleep(WAIT_A_SEC)
    # alerts_res = requests.post(url=END_POINT_URL) #GET ALERTS
    alerts=[ {"alert_id":"guid","commands": [{"id":"warehouses","sql":"show warehouses; "},{"id":"roles","sql":"show roles "} ]} ]

    for alert in alerts:
        send_obj={}
        for command in alert['commands']:
            for account in accounts:

                # Connecting to Snowflake using the default authenticator
                cnx = snowflake.connector.connect(
                    account=account['host'],
                    user=account['user'],
                    password=account['password']
                )

                #Get Queries
                sql = command['sql']

                cur_res = cnx.cursor().execute(sql)

                send_obj={}

                rows=[]
                for  val in cur_res:
                    row_obj={}
                    for idx,col in enumerate(cur_res._description):
                        row_obj[col[0]] = val[idx]
                    rows.append(row_obj)

                send_obj[command['id']]= rows

        # alerts_res = requests.post(url=END_POINT_URL) #GET ALERTS
        print(send_obj)


if __name__ == '__main__':


    accounts = [{"host": "account.region", "display_name": "info", "user": "john", "password": "**"}]

    run('<YOUR_API_TOKEN>', accounts)
