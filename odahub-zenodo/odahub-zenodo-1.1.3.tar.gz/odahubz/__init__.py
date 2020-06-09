import os
import json
import requests

def get_auth():
    read_file = lambda x:dict(zip(['zenodo_endpoint', 'token'],[l.strip() for l in open(x)]))

    methods_failed=[]
    for comment, method in [
        ("", lambda: read_file(os.path.join(os.environ.get('HOME'), '.zenodo-token-odahub-sandbox'))),
        ("", lambda: read_file('/cdci-resources/zenodo-token-odahub-sandbox')),
    ]:
        try:
            return method()
        except Exception as e:
            methods_failed.append("method {} failed: {}".format(comment, repr(e)))
            print(methods_failed[-1])

    raise Exception('unable to find auth:', methods_failed)
        

def publish(title, fn_png, provenance):
    auth = get_auth()
    ACCESS_TOKEN = auth['token']
    ENDPOINT = auth['zenodo_endpoint']


    r = requests.get(ENDPOINT+"/api/deposit/depositions",
                      params={'access_token': ACCESS_TOKEN},
                    )

    print(r.status_code)
    print(r.json())

    r = requests.post(ENDPOINT+"/api/deposit/depositions",
                      params={'access_token': ACCESS_TOKEN},
                      headers = {"Content-Type": "application/json"},
                      json={},   
                    )

    print(r.status_code)
    print(r.json())


    deposition_id = r.json()['id']

    data = {'filename': os.path.basename(fn_png)}
    files = {
                'file': open(fn_png, 'rb'),
            }

    r = requests.post(ENDPOINT+'/api/deposit/depositions/%s/files' % deposition_id,
                       params={'access_token': ACCESS_TOKEN}, 
                       data=data,
                       files=files)

    print(r.status_code)
    print(r.json())

    data = {
        'metadata': {
            'title': title,
            'upload_type': 'image',
            'image_type': 'plot',
            'description': 'provenance: '+provenance+" ontology: x",
            'creators': [{'name': 'INTEGRAL',
                          'affiliation': 'ESA'}]
        }
    }

    r = requests.put(ENDPOINT+'/api/deposit/depositions/%s' % deposition_id,
                     params={'access_token': ACCESS_TOKEN}, data=json.dumps(data),
                     headers = {"Content-Type": "application/json"})

    print(r.status_code)
    print(r.json())

    r = requests.post(ENDPOINT+'/api/deposit/depositions/%s/actions/publish' % deposition_id,
                      params={'access_token': ACCESS_TOKEN} )

    print(r.status_code)
    print(r.json())

    print(r.json()['links']['latest_html'])

