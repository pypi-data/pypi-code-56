import requests
import json


class requestMode(object):  # ff
    post = "post"
    get = "get"
    put = "put"
    delete = "delete"


def sendRequest(
    url, header="", params="", content="", rMode=requestMode.post, files=""
):

    if rMode == "post":
        rMode = requests.post
    elif rMode == "get":
        rMode = requests.get
    elif rMode == "put":
        rMode = requests.put
    elif rMode == "delete":
        rMode = requests.delete

    status = True

    content = (
        json.dumps(content) if isinstance(content, (list, dict)) else content
    )

    try:
        response = rMode(
            url=url,
            headers=header,
            params=params,
            files=files,
            data=content,
        )
        if response.status_code < 300 and response.status_code >= 200:
            status = True
        else:
            status = False
        content = response.content

    except requests.exceptions.RequestException:
        status = False
        content = '%s Request failed' % url

    return (status, content)
