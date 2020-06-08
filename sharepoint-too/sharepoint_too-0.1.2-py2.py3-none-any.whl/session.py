import json
import re
from datetime import datetime, timedelta
from urllib import parse
from pathlib import Path

import requests
from requests_ntlm import HttpNtlmAuth

# https://docs.microsoft.com/en-us/sharepoint/dev/sp-add-ins/working-with-lists-and-list-items-with-rest


class SharePointSession(requests.Session):
    """A SharePoint Requests session.
    Provide session authentication to SharePoint Online sites
    in addition to standard functionality provided by Requests.
    Basic Usage::
      >>> from sharepoint import SharePointSession
      >>> sp = SharePointSessiont("example.sharepoint.com", "username", "password")
      >>> sp.get_lists()
      <Response [200]>
    """

    def __init__(self, site=None, username=None, password=None):
        super().__init__()

        self.site = re.sub(r"^https?://", "", site)
        self.expire = datetime.now()

        # print(f"Site: {self.site}")
        # print(f"Expire: {self.expire}")

        self.username = username
        self.password = password

        self.auth = HttpNtlmAuth(self.username, self.password)
        # Add required headers for communicating with SharePoint
        self.headers.update(
            {
                "accept": "application/json;odata=verbose",
                "content-type": "application/json;odata=verbose",
            }
        )

        self._redigest()

    def _redigest(self):
        """"Check and refresh site's request form digest"""

        if self.expire <= datetime.now():
            # print("=> Requesting form digest value...")
            # Avoid recursion error by not using the self.post as we call `_redigest()` in `post()`
            auth = HttpNtlmAuth(self.username, self.password)
            headers = {
                "accept": "application/json;odata=verbose",
                "content-type": "application/json;odata=verbose",
            }
            url = f"https://{self.site}/_api/contextinfo"
            # print(f"API contextinfo URL: {url}")
            r = requests.post(url, headers=headers, auth=auth)
            response = r.json()

            # self.headers.update({"Cookie": self._buildcookie(r.cookies)})
            # # print(r.cookies.get_dict())

            # Parse digest text and timeout
            ctx = response["d"]["GetContextWebInformation"]
            self.digest = ctx["FormDigestValue"]
            timeout = ctx["FormDigestTimeoutSeconds"]

            # Calculate digest expiry time
            self.expire = datetime.now() + timedelta(seconds=timeout)

            # print(f"Digest: {self.digest}")
            # print(f"Timeout: {timeout}")
            # print(f"Expire: {self.expire}")

            # Update the session headers with the digest
            # print("=> Update x-requestdigest value ...")
            self.headers.update({"x-requestdigest": self.digest})

        # print(f"Current Digest: {self.digest}")
        return self.digest

    def post(self, url, *args, **kwargs):
        """Make POST request and include x-requestdigest header"""
        # print(f"=> POST: {url}")
        if "headers" in kwargs.keys():
             kwargs["headers"].update(**kwargs["headers"])
        # self.headers.update({"Authorization": "Bearer " + self._redigest()})
        self.headers.update({"x-requestdigest": self._redigest()})
        return super().post(url, *args, **kwargs)

    # def get(self, url, *args, **kwargs):
    #     """Make GET request and include x-requestdigest header"""
    #     # print(f"=> GET: {url}")
    #     if "headers" in kwargs.keys():
    #         kwargs["headers"].update(**kwargs["headers"])
    #     # self.headers.update({"Authorization": "Bearer " + self._redigest()})
    #     self.headers.update({"x-requestdigest": self._redigest()})
    #     return super().get(url, *args, **kwargs)

    # --------------------------------------------------------------------------
    # Helper methods
    # --------------------------------------------------------------------------

    # def get_file(self, url, *args, **kwargs):
    #     """Stream download of specified URL and output to file"""
    #     # Extract file name from request URL if not provided as keyword argument
    #     filename = kwargs.pop("filename", re.search(r"[^/]+$", url).group(0))
    #     kwargs["stream"] = True
    #     # Request file in stream mode
    #     r = self.get(url, *args, **kwargs)
    #     # Save to output file
    #     if r.status_code == requests.codes.ok:
    #         with open(filename, "wb") as file:
    #             for chunk in r:
    #                 file.write(chunk)
    #     return r

    def get_lists(self, weblist_url, **kwargs):
        """Get lists."""
        return self.get(weblist_url, **kwargs)

    def get_list_metadata(
        self, weblist_url, list_guid=None, list_title=None, **kwargs
    ):
        """Get list metadata."""
        if list_guid is None and list_title is None:
            raise ValueError("Either `list_guid` or `list_title` must be set.")
        if list_guid and list_title:
            raise ValueError(
                "Either `list_guid` or `list_title` must be set, not both."
            )
        if list_guid:
            url = f"{weblist_url}(guid'{list_guid}')"
        else:
            list_title = parse.quote(list_title)
            url = f"{weblist_url}/getbytitle('{list_title}')"
        return self.get(url, **kwargs)

    def get_list_entity_type(
        self, weblist_url, list_guid=None, list_title=None, **kwargs
    ):
        """Need to get the list item type in order to add/update it."""
        if list_guid is None and list_title is None:
            raise ValueError("Either `list_guid` or `list_title` must be set.")
        if list_guid and list_title:
            raise ValueError(
                "Either `list_guid` or `list_title` must be set, not both."
            )
        if list_guid:
            url = f"{weblist_url}(guid'{list_guid}')?$select=ListItemEntityTypeFullName"
        else:
            list_title = parse.quote(list_title)
            url = f"{weblist_url}/getbytitle('{list_title}')?$select=ListItemEntityTypeFullName"
        return self.get(url, **kwargs)

    def get_list_items(self, weblist_url, list_guid=None, list_title=None, **kwargs):
        """Retrieve all list items."""
        if list_guid is None and list_title is None:
            raise ValueError("Either `list_guid` or `list_title` must be set.")
        if list_guid and list_title:
            raise ValueError(
                "Either `list_guid` or `list_title` must be set, not both."
            )
        if list_guid:
            url = f"{weblist_url}(guid'{list_guid}')/items"
        else:
            list_title = parse.quote(list_title)
            url = f"{weblist_url}/getbytitle('{list_title}')/items"
        return self.get(url, **kwargs)

    def get_list_item(
        self, weblist_url, item_id, list_guid=None, list_title=None, **kwargs
    ):
        """Retrieve specific list item."""
        if list_guid is None and list_title is None:
            raise ValueError("Either `list_guid` or `list_title` must be set.")
        if list_guid and list_title:
            raise ValueError(
                "Either `list_guid` or `list_title` must be set, not both."
            )
        if list_guid:
            url = f"{weblist_url}(guid'{list_guid}')/items({item_id})"
        else:
            list_title = parse.quote(list_title)
            url = f"{weblist_url}/getbytitle('{list_title}')/items({item_id})"
        return self.get(url, **kwargs)

    def add_list_item(
        self, weblist_url, payload, list_guid=None, list_title=None, headers={}
    ):
        """Add list item."""
        if list_guid is None and list_title is None:
            raise ValueError("Either `list_guid` or `list_title` must be set.")
        if list_guid and list_title:
            raise ValueError(
                "Either `list_guid` or `list_title` must be set, not both."
            )
        if list_guid:
            url = f"{weblist_url}(guid'{list_guid}')/items"
        else:
            list_title = parse.quote(list_title)
            url = f"{weblist_url}/getbytitle('{list_title}')/items"
        return self.post(url, json=payload, headers=headers)

    def update_list_item(
        self, weblist_url, item_id, data, list_guid=None, list_title=None, headers={}
    ):
        """Update a specific list item."""
        if list_guid is None and list_title is None:
            raise ValueError("Either `list_guid` or `list_title` must be set.")
        if list_guid and list_title:
            raise ValueError(
                "Either `list_guid` or `list_title` must be set, not both."
            )
        if list_guid:
            url = f"{weblist_url}(guid'{list_guid}')/items({item_id})"
        else:
            list_title = parse.quote(list_title)
            url = f"{weblist_url}/getbytitle('{list_title}')/items({item_id})"
        headers.update({"x-http-method": "MERGE", "if-match": "*"})
        # Update with any supplied headers
        headers.update(**headers)
        return self.post(url, json=data, headers=headers)

    def upload(
        self,
        weblist_url,
        item_id,
        filename,
        list_guid=None,
        list_title=None,
        headers={},
    ):
        """Upload a file to a list item."""
        if list_guid is None and list_title is None:
            raise ValueError("Either `list_guid` or `list_title` must be set.")
        if list_guid and list_title:
            raise ValueError(
                "Either `list_guid` or `list_title` must be set, not both."
            )

        uploaded_filename = Path(filename).name
        if list_guid:
            url = (
                f"{weblist_url}(guid'{list_guid}')/items({item_id})"
                f"/AttachmentFiles/add(FileName='{uploaded_filename}')"
            )
        else:
            list_title = parse.quote(list_title)
            url = (
                f"{weblist_url}/getbytitle('{list_title}')/items({item_id})"
                f"/AttachmentFiles/add(FileName='{uploaded_filename}')"
            )
            print(url)
        # Perform the actual upload
        with open(filename, "rb") as fp:
            content = fp.read()

        # Add the content-length
        headers.update({"content-length": str(len(content))})
        # Update with any supplied headers
        headers.update(**headers)
        return self.post(url, data=content, headers=headers)

    def delete_list_item(
        self, weblist_url, item_id, list_guid=None, list_title=None, headers={}
    ):
        """Delete a specific list item."""
        if list_guid is None and list_title is None:
            raise ValueError("Either `list_guid` or `list_title` must be set.")
        if list_guid and list_title:
            raise ValueError(
                "Either `list_guid` or `list_title` must be set, not both."
            )
        if list_guid:
            url = f"{weblist_url}(guid'{list_guid}')/items({item_id})"
        else:
            list_title = parse.quote(list_title)
            url = f"{weblist_url}/getbytitle('{list_title}')/items({item_id})"
        headers.update({"x-http-method": "DELETE", "if-match": "*"})
        # Update with any supplied headers
        headers.update(**headers)
        return self.post(url, headers=headers)


#     def _buildcookie(self, cookies):
#         """Create session cookie from response cookie dictionary"""
#         return "rtFa=" + cookies["rtFa"] + "; FedAuth=" + cookies["FedAuth"]
