"""
.. See the NOTICE file distributed with this work for additional information
   regarding copyright ownership.
   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at
       http://www.apache.org/licenses/LICENSE-2.0
   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

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