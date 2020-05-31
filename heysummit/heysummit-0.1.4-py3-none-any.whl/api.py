import requests


class HeySummitException(Exception):
    """Base Class for API Exceptions"""

    pass


class HeySummit(object):
    def __init__(self, token=None, debug=False):
        if token is None:
            raise HeySummitException(
                "HeySummit API Client needs a token to work properly"
            )

        self.api_token = token
        self.api_endpoint = "https://api.heysummit.com/api"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": "Token {0}".format(self.api_token),
        }

        self.debug = debug
        self.client = requests.Session()

    def _request(self, action="GET", url="/", json=None, headers=None, params=None):
        """ Helper class for calling requests """
        if url.startswith("https"):
            endpoint = url
        else:
            endpoint = self.api_endpoint + url

        # Output HTTP dialog if using debug mode
        if self.debug:
            import http.client as http_client

            http_client.HTTPConnection.debuglevel = 1

        return self.client.request(
            method=action, url=endpoint, headers=self.headers, params=params, json=json
        )

    def _get_paged_results(self, response=None, params=None):
        """ Helper class for iterating over pages and returning all results """

        next_page = response.json()["next"]
        results = response.json()["results"]

        # Get all results, iterating over pagination
        while next_page and len(results) > 0:
            r = self._request(url=next_page, params=params)
            # Raise if there is any problem
            r.raise_for_status

            next_page = r.json()["next"]
            results += r.json()["results"]

        return results

    def get_events(
        self,
        is_live=False,
        is_archived=False,
        is_evergreen=False,
        is_open_for_registrations=False,
    ):
        """Gets all events

      Args:
         is_live (bool):  filter for live events
         is_archive (bool):  filter for archived events
         is_evergreen (bool):  filter for evergreen events
         is_open_for_registrations (bool):  filter for open for registration events


      Returns:
         [json].  The events list::

      Raises:
         RequestsError

      This endpoint retrieves all Events linked to your account.

      >>> from heysummit.api import HeySummit, HeySummitException
      >>> hey = HeySummit(token=<yourtoken>)
      >>> print(hey.get_events())

      """
        params = {}
        if is_live:
            params["is_live"] = is_live
        if is_archived:
            params["is_archived"] = is_archived
        if is_evergreen:
            params["is_evergreen"] = is_evergreen
        if is_open_for_registrations:
            params["is_open_for_registrations"] = is_open_for_registrations

        r = self._request(url="/events/", params=params)

        r.raise_for_status

        return self._get_paged_results(response=r, params=params)

    def get_talks(self, event=None, is_active=None):
        """Gets all talks

      Args:
         event (int): 	The ID of the Event you want to filter the Talks list by
         is_active (bool) 	Set this to True to filter Talks that are currently marked as Active (or not)

      Returns:
         [json].  The talks list::

      Raises:
         RequestsError

      This endpoint retrieves all Talks with the specified filters.

      >>> from heysummit.api import HeySummit, HeySummitException
      >>> hey = HeySummit(token=<yourtoken>)
      >>> print(hey.get_talks())


      """

        params = {}

        if event is not None:
            params["event"] = event

        if is_active is not None:
            params["is_active"] = is_active

        r = self._request(url="/talks", params=params)

        r.raise_for_status

        return self._get_paged_results(response=r, params=params)

    def get_attendees(self, event=None):
        """Gets all attendees

        Args:
            event (int): 	The ID of the Event you want to filter the attendees list by

        Returns:
            [json].  The attendees list::

        Raises:
            RequestsError

        This endpoint retrieves all Attendees with the specified filters.

        >>> from heysummit.api import HeySummit, HeySummitException
        >>> hey = HeySummit(token=<yourtoken>)
        >>> print(hey.get_attendees())

        """

        params = {}

        if event is not None:
            params["event"] = event

        r = self._request(url="/attendees", params=params)

        r.raise_for_status

        return self._get_paged_results(response=r, params=params)

    def get_attendee(self, id=None):
        """Gets attendee information

         Args:
            id (int): 	The ID of the Attendee you want

         Returns:
            None   No ticket could be found with that ID.
            json.  The attendee::

         Raises:
            RequestsError

          This endpoint retrieves a spcific Attendee.

          >>> from heysummit.api import HeySummit, HeySummitException
          >>> hey = HeySummit(token=<yourtoken>)
          >>> print(hey.get_attendee())

        """

        if id is None:
            return None

        r = self._request(url="/attendees/{id}".format(id=id))

        if r.status_code == 404:
            return None

        r.raise_for_status

        return r.json()

    def add_attendee(self, event=None, email=None, name=None):
        """Adds attendee to event

         Args:
            event (int): 	The ID of the Event you want the attendee added
            email (string): The attendee's email
            name  (string): The attendee's name

         Returns:
            id.  The created attendee id::

         Raises:
            RequestsError
            HeySummitException

          Please note that once the Attendee has been added, you may still need to add them to Talks.
          It is also assumed that any Attendee added, has accepted your terms and conditions and has agreed to be added to this Event and emailed regarding the event (with reminders and notifications relating to the talks they are booked into).

          >>> from heysummit.api import HeySummit, HeySummitException
          >>> hey = HeySummit(token=<yourtoken>)
          >>> attendee = hey.add_attendee(event=5573, email="you@example.com", name="Test Me")

         """

        if event is None or email is None or name is None:
            raise HeySummitException("Add attendee needs all parameters to work")

        data = {"event": event, "email": email, "name": name}

        r = self._request(action="POST", url="/attendees/", json=data)

        r.raise_for_status

        if r.status_code == 201:  # HTTP/1.1 201 Created
            return True
        else:
            return False

    def get_tickets(self, event=None):
        """Gets all attendees

        Args:
            event (int): 	The ID of the Event you want to filter the attendees list by

        Returns:
            [json].  The attendees list::

        Raises:
            RequestsError

        This endpoint retrieves all Attendees with the specified filters.

        >>> from heysummit.api import HeySummit, HeySummitException
        >>> hey = HeySummit(token=<yourtoken>)
        >>> print(hey.get_attendees())

        """

        params = {}

        if event is not None:
            params["event"] = event

        r = self._request(url="/tickets", params=params)

        r.raise_for_status

        return self._get_paged_results(response=r, params=params)

    def get_ticket(self, id=None):
        """Gets ticket information

         Args:
            id (int): 	The ID of the Attendee you want

         Returns:
            None   No ticket could be found with that ID.
            json.  The ticket for the attendee id::

         Raises:
            RequestsError

          This endpoint retrieves a spcific Attendee.

          >>> from heysummit.api import HeySummit, HeySummitException
          >>> hey = HeySummit(token=<yourtoken>)
          >>> print(hey.get_attendee())

         """

        if id is None:
            return None

        r = self._request(url="/tickets/{id}/".format(id=id))

        if r.status_code == 404:
            return None

        r.raise_for_status

        return r.json()
