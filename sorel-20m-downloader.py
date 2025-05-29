import xml.etree.ElementTree as ET
import urllib.request as REQ
import os
import time
import requests

sorel_url = "http://sorel-20m.s3.amazonaws.com/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
    "Accept-Encoding": "*",
    "Connection": "keep-alive",
}

page = requests.get(sorel_url, headers=headers)

sorel_20m = {"sorel_20m": "http://s3.amazonaws.com/doc/2006-03-01/"}

os.makedirs("bin", exist_ok=True)

downloaded = 0
limit = 3000000
prefix = "09-DEC-2020/binaries/"
prefix_len = len(prefix)

tree = ET.parse(sorel_xml)
root = tree.getroot()
for contents in root.findall("sorel_20m:Contents", sorel_20m):
    key = contents.find("sorel_20m:Key", sorel_20m)

    if key.text[:prefix_len] == prefix:
        size = int(contents.find("sorel_20m:Size", sorel_20m).text)
        if (downloaded + size) >= limit:
            break
        name = key.text[prefix_len:]
        if os.path.exists("bin/" + name) == False:
            # Download the file from `url` and save it locally under `file_name`:
            with REQ.urlopen(sorel_url + key.text) as response, open("bin/" + name, 'wb') as out_file:
                shutil.copyfileobj(response, out_file)
            time.sleep(1)

        downloaded = downloaded + size

print(downloaded)
