from aiohttp import ClientSession, ClientResponseError


class PoolSense:
    """Main Interface to the Poolsense Device"""

    def __init__(self):
        self._version = "0.0.4"
        self._url_login = 'https://api.poolsense.net/api/v1/users/login'


    async def test_poolsense_credentials(self, session: ClientSession, username, password):
        """Function tests the credentials against the Poolsense Servers"""
        
        LOGIN_DATA = {
            "email": username,
            "password": password,
            "uuid": "26aab38027422a59",
            "registrationId": "c5tknccIS_I:APA91bF0LS4mAR2NETBJ9tNFYEbvUgileRovnuC1Y9-yTy2qDsW4_YHlDcapH7BnHWzxh74fPVJw0Y9KuM3sCVIWknSOlGu3WP0QNSFzfuhEwQ_yBujt9cSVak0eVUo_IfmFf6rtlng_"
        }

        # """Login to the system."""
        resp = await session.post(self._url_login, json=LOGIN_DATA)
        if resp.status == 200:
            data = await resp.json(content_type=None)
            print(data)
            if data["token"] is None:
                return False
            else:
                return True
        else:
            return False


    async def get_poolsense_data(self, session: ClientSession, username, password):
        """Function gets all the data for this user account from the Poolsense servers"""
        LOGIN_DATA = {
            "email": username,
            "password": password,
            "uuid": "26aab38027422a59",
            "registrationId": "c5tknccIS_I:APA91bF0LS4mAR2NETBJ9tNFYEbvUgileRovnuC1Y9-yTy2qDsW4_YHlDcapH7BnHWzxh74fPVJw0Y9KuM3sCVIWknSOlGu3WP0QNSFzfuhEwQ_yBujt9cSVak0eVUo_IfmFf6rtlng_"
        }

        # """Login to the system."""
        resp = await session.post(self._url_login, json=LOGIN_DATA)
        data = await resp.json(content_type=None)

        URL_DATA = 'https://api.poolsense.net/api/v1/sigfoxData/app/' + data['devices'][0]["serial"] + '/?tz=-120'
        head = {'Authorization': 'token {}'.format(data["token"])}

        #
        resp = await session.get(URL_DATA, headers=head)
        data = await resp.json(content_type=None)
        #     # API does not set correct status header so we manually check.
        #     raise ClientResponseError(
        #         resp.request_info,
        #         resp.history,
        #         status=data['error']['code'],
        #         message=data['error']['message'],
        #         headers=resp.headers
        #     )

        results = {
            "Chlorine": data["ORP"],
            "pH": data["pH"],
            "Water Temp": data["waterTemp"],
            "Battery": data["vBat"],
            "Last Seen": data["lastData"]["time"],
            "Chlorine High": data["display"]["orpNotificationMax"],
            "Chlorine Low": data["display"]["orpNotificationMin"],
            "pH High": data["display"]["phNotificationMax"],
            "pH Low": data["display"]["phNotificationMin"],
            "pH Status": data["display"]["pHColor"],
            "Chlorine Status": data["display"]["ORPColor"]
        }
        # for item in data["features"]:
        #     try:
        #         results.append(source.from_json(item))
        #     except KeyError:
        #         logging.getLogger(__name__).warning("Got wrong data: %s", item)

        return results
