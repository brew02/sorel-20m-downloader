import xml.etree.ElementTree as ET
import os
import time
import requests
import boto3
from botocore import UNSIGNED
from botocore.config import Config

s3 = boto3.client("s3", config=Config(signature_version=UNSIGNED))

sorel_xml = requests.get("http://sorel-20m.s3.amazonaws.com/")
os.makedirs("bin", exist_ok=True)


downloaded = 0
limit = 3000000 # Set limit to 3MB
prefix = "09-DEC-2020/binaries/"
prefix_len = len(prefix)
sorel_20m = {"sorel_20m": "http://s3.amazonaws.com/doc/2006-03-01/"}

root = ET.fromstring(sorel_xml.text)

# TODO: To get more binaries, use the last key returned in the
# XML as the marker parameter in the URL request
for contents in root.findall("sorel_20m:Contents", sorel_20m):
    key = contents.find("sorel_20m:Key", sorel_20m)

    if key.text[:prefix_len] == prefix:
        size = int(contents.find("sorel_20m:Size", sorel_20m).text)
        if (downloaded + size) > limit:
            break
        
        binary_name = key.text[prefix_len:]
        if os.path.exists("bin/" + binary_name) == False:
            s3.download_file("sorel-20m", prefix + binary_name, "bin/" + binary_name)

        downloaded = downloaded + size

print(downloaded)
