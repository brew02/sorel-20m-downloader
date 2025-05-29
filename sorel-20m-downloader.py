import xml.etree.ElementTree as ET
import os
import requests
import boto3
from botocore import UNSIGNED
from botocore.config import Config

# Open a new AWS S3 boto3 client without authentication
s3 = boto3.client("s3", config=Config(signature_version=UNSIGNED))
# Make the bin directory if it doesn't exist
os.makedirs("bin", exist_ok=True)

# Prefix for keys that represent binaries
prefix = "09-DEC-2020/binaries/" 
prefix_len = len(prefix)

# Use the prefix in the URL parameters. This way
# we only get objects that represent binaries
params = {"prefix": prefix}

num_down = 0
bytes_down = 0
total_bin_size = 0
# Set binary download limit to 30MB
limit = 30000000 

# xmlns namespace
namespace = {"namespace": "http://s3.amazonaws.com/doc/2006-03-01/"}

while True:
    # Download the XML file from AWS (you can view this XML file by
    # pasting the URL into your browser)
    sorel_xml = requests.get("http://sorel-20m.s3.amazonaws.com/", params=params)
    # Create the root from the XML file
    root = ET.fromstring(sorel_xml.text)

    done = False

    # For each Contents element from the root
    for contents in root.findall("namespace:Contents", namespace):
        # Get the Key element
        key = contents.find("namespace:Key", namespace)
        # Update the marker in case the XML was truncated
        params["marker"] = key

        # Get the binary size
        size = int(contents.find("namespace:Size", namespace).text)
        if (total_bin_size + size) > limit:
            done = True
            break
        
        # Get the name of the binary
        binary_name = key.text[prefix_len:]
        
        # If the binary hasn't been downloaded yet, download it
        if os.path.exists("bin/" + binary_name) == False:
            s3.download_file("sorel-20m", prefix + binary_name, "bin/" + binary_name)
            bytes_down = bytes_down + size
            num_down = num_down + 1

        total_bin_size = total_bin_size + size

    if done:
        break

    # If the data was truncated and we aren't done,
    # request the next piece of data, otherwise break
    is_truncated = root.find("namespace:IsTruncated", namespace).text == "True"
    if is_truncated == False:
        break

# Print summary
print("Downloaded " + str(num_down) + " binaries: " + str(bytes_down) + " bytes")
