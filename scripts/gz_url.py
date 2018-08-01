from __future__ import print_function
import xml.etree.ElementTree as ET
import requests
import sys


def xml_download(accession):
    xml = ET.fromstring(requests.get("https://www.ebi.ac.uk/ena/data/view/{}&display=xml".format(accession),
                                     stream=True, timeout=60).content)
    return xml


if __name__ == "__main__":
    for i in xml_download(sys.argv[1]).find("ASSEMBLY").find("ASSEMBLY_LINKS").findall("ASSEMBLY_LINK"):
        if i.find("URL_LINK").find("LABEL").text == "WGS_SET_FASTA":
            print("url=" + i.find("URL_LINK").find("URL").text)