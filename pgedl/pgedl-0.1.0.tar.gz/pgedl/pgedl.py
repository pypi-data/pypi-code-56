import base64
import requests
import shutil
import json
import glob
from pathlib import Path
import argparse

def dl_path():
    p = Path.home().joinpath(".gearth")
    if not p.exists:
        p.mkdir()
    return str(p)    

def download_image(i):
    p = dl_path()
    fn = f"{p}/{i}"

    r = requests.get(f"https://www.gstatic.com/prettyearth/assets/data/v2/{i}.json")
    
    if r.status_code == 200:
        j = r.json()
        u = j["dataUri"]
        head = "data:image/jpeg;base64,"
        d = {k: j[k] for k in j if k != "dataUri"}
        if u[:23] == head:
            img = base64.b64decode(u[23:])
            p = dl_path()
            with open(f"{fn}.jpg", "wb") as o:
                o.write(img)
            with open(f"{fn}.json", "w") as o:
                o.write(json.dumps(d, indent=4, ensure_ascii=False))
            print(f"Image downloaded to '{fn}.jpg', metadata to '{fn}.json'")
    else:
        r = requests.get(f"https://www.gstatic.com/prettyearth/assets/full/{i}.jpg",
                         stream=True)
        if r.status_code == 200:
            with open(f"{fn}.jpg", "wb") as o:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, o)  
            print(f"Image downloaded to '{fn}.jpg', no metadata found.'")
        else:
            print(f"Image {i} not found, sorry!")

def run():
    parser = argparse.ArgumentParser(description="Download Pretty Google Earth wallpapers.")
    parser.add_argument("id", metavar='id', type=int,
                        help='the id of the wallpaper to be downloaded (e.g. 6311')
    args = parser.parse_args()

    download_image(args.id)
