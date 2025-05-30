# SOREL-20M Binary Downloader

This Python script downloads the PE files from the SOREL-20M dataset using the given limit in bytes. The PE files are compressed using zlib. An easy way to decompress the files is with the following command:
`openssl zlib -d < [filename] > [output_filename]`

## Prerequisites

Ensure that requests and boto3 is installed using the following command:

`pip install requests boto3`
