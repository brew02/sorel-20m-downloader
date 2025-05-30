# SOREL-20M Binary Downloader

This Python script downloads the PE binaries from the SOREL-20M dataset with a byte limit in the script so that only a fraction of the 8 TBs is downloaded. The PE binaries are compressed using zlib. An easy way to decompress the files is with the following command:
`openssl zlib -d < [filename] > [output_filename]`

## Prerequisites

Ensure that requests and boto3 is installed using the following command:

`pip install requests boto3`
