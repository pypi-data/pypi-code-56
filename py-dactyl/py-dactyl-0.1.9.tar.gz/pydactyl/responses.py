"""Classes used for creating responses."""


class PaginatedResponse(object):
    """An iterable API response that returns paginated results."""

    def __init__(self, client, endpoint, data):
        self._client = client
        self._initial_data = data['data']
        self.data = data
        self.endpoint = endpoint
        self.meta = data['meta']

    def __getitem__(self, item):
        if hasattr(self, item):
            return getattr(self, item, None)
        raise KeyError(item)

    def __iter__(self):
        self._iteration = 0
        self.data = self._initial_data
        return self

    def __next__(self):
        """"Retrieves the next page of results.

        Returns:
            object: An instance of PaginatedResponse

        Raises:
            PterodactylApiError: If the API request fails
            StopIteration: When the next page does not exist.
        """
        self._iteration += 1
        if self._iteration == 1:
            return self
        if self._next_page_exists(self.meta):
            params = {'page': self._iteration}
            response = self._client._api_request(endpoint=self.endpoint,
                                                 params=params)
            self.data = response['data']
            self.meta = response['meta']
            return self
        else:
            raise StopIteration

    def __str__(self):
        return '%s' % self.data

    def get(self, key, default=None):
        """Retrieves a key from the response data.

        Returns:
            Value for the specified key
        """
        return getattr(self, key, default)

    def get_next_page_link(self):
        """Get a link to the next page.

        Returns:
            str: Link provided by API
        """
        return self.meta['pagination']['links'].get('next')

    def get_previous_page_link(self):
        """Get a link to the previous page.

        Returns:
            str: Link provided by API
        """
        return self.meta['pagination']['links'].get('previous')

    @staticmethod
    def _next_page_exists(data):
        """Determine if the response contains a valid link to the next page.

        Returns:
            bool: True if next page exists.
        """
        exists = ('pagination' in data
                  and 'links' in data['pagination']
                  and 'next' in data['pagination']['links']
                  and data['pagination']['links']['next'] != '')
        return exists
