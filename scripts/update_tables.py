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

import ast
import sys
import xml.etree.ElementTree as ET
from datetime import datetime

import requests
from sqlalchemy import create_engine, Table, MetaData, func, or_
from sqlalchemy.orm import sessionmaker

from base import *

# setup config
config_path = sys.argv[1]

with open(config_path) as configfile:
    config = ast.literal_eval(configfile.read())

tony_assembly = config["tony_assembly"]
results_dir = config ["results_dir"]
udocker_root = config["udocker_root"]
toil_dir = config["toil_dir"]
workflow_dir = config["workflow_dir"]
log_dir = config["log_dir"]
registry = config["registry"]


def xml_download(ena_accession):
    """
    pulling xml record from ENA
    :param ena_accession:
    :return:
    """
    try:
        xml = ET.fromstring(requests.get("https://www.ebi.ac.uk/ena/data/view/{}&display=xml".format(ena_accession),
                                         stream=True, timeout=60).content)
        return xml
    except requests.exceptions.ReadTimeout:
        stderr.write("Could not download XML file with accession {}\n".format(ena_accession))
        return None


def xml_download_retry(ena_accession):
    """
    pulling xml record from ENA, some of the records take a longer time to connect, this retry set timeout to be 5 mins
    :param ena_accession:
    :return:
    """
    try:
        xml = ET.fromstring(requests.get("https://www.ebi.ac.uk/ena/data/view/{}&display=xml".format(ena_accession),
                                         stream=True, timeout=300).content)
        return xml
    except requests.exceptions.ReadTimeout:
        stderr.write("Could not download XML file with accession {}\n".format(ena_accession))
        return None


def chromosome_number(xml):
    """
    find the number of chromosomes within the assembly. If the assembly is assembled to scaffold level, returns 0
    :param xml:
    :return:
    """
    try:
        chroms_number = len(xml.find("ASSEMBLY").find("CHROMOSOMES").findall("CHROMOSOME"))
        return chroms_number
    except AttributeError:
        return 0


def get_chromosomes(xml):
    for record in xml.find("ASSEMBLY").find("CHROMOSOMES").findall("CHROMOSOME"):
        yield record


def chromosome_data(xml):
    """
    extract md5 and length of the chromosome from the chromosome's xml record
    :param xml:
    :return:
    """
    for xref in xml.find("entry").findall("xref"):
        if xref.attrib["db"] == "MD5":
            md5 = xref.attrib["id"]
        break
    length = xml.find("entry").attrib["sequenceLength"]
    return md5, int(length)


def get_scaffold_number(xml):
    for attribute in xml.find("ASSEMBLY").find("ASSEMBLY_ATTRIBUTES").findall("ASSEMBLY_ATTRIBUTE"):
        if attribute.find("TAG").text == "scaffold-count":
            return int(attribute.find("VALUE").text)


stderr = open("{log_dir}/log_update_tables.txt".format(log_dir=log_dir), "a")
stderr.write(str(datetime.now()) + "\n")
stderr.write("====\n")
registry_engine = create_engine(registry)
assembly = Table("assembly", MetaData(), autoload=True, autoload_with=registry_engine)
engine = create_engine(tony_assembly)
session = sessionmaker(bind=engine)
s = session()
old_accessions = s.query(GCA.accession).all()

r_session = sessionmaker(bind=registry_engine)
rs = r_session()
sub_concat = func.concat(assembly.c.chain, ".", assembly.c.version)
new_accessions = rs.query(sub_concat).filter(sub_concat.notin_(old_accessions)).all()
rs.close()
s = session()
for entry in new_accessions:
    gca = GCA()
    gca.accession = entry[0]
    # print(gca.accession)
    gca_xml = xml_download(gca.accession)
    if gca_xml is not None:  # only add to GCA table if the xml record of the assembly exists
        try:
            gca.assembly_level = gca_xml.find("ASSEMBLY").find("ASSEMBLY_LEVEL").text
        except AttributeError:
            gca.assembly_level = "No Level"
            stderr.write("{} has no assembly_level attribute, not added to database\n".format(gca.accession))
        if gca.assembly_level in ["chromosome", "complete genome"]:
            gca.records = chromosome_number(gca_xml)
            s.add(gca)
            # print(gca.accession, gca.assembly_level, gca.records)
            for chrom_record in get_chromosomes(gca_xml):
                chromosome = Chromosome()
                chromosome.GCA_accession = gca.accession
                chromosome.accession = chrom_record.attrib["accession"]
                # print(chromosome.accession)
                chromosome.name = chrom_record.find("NAME").text
                chromosome.status = 1
                chrom_xml = xml_download(chromosome.accession)
                if chrom_xml is not None:
                    try:
                        chromosome.md5, chromosome.length = chromosome_data(chrom_xml)
                    except AttributeError:
                        stderr.write("Chromosome {} doesn't exit or has corrupted xml file. Chromosome was added "
                                     "without md5 and length.\n".format(chromosome.accession))
                s.add(chromosome)
                # print(chromosome.accession, chromosome.GCA_accession,
                #  chromosome.name, chromosome.length, chromosome.md5)
                if not s.query(Jobs).filter(Jobs.chromosome_accession == chromosome.accession).all():
                    for job in ["get_fasta", "GC", "trf", "CpG"]:
                        s.add(Jobs(chromosome_accession=chromosome.accession,
                                   job_name=job))
                        # print(chromosome.accession, job)
        elif gca.assembly_level in ["scaffold", "contig"]:
            gca.records = get_scaffold_number(gca_xml)
            s.add(gca)
            for job in ["get_fasta", "GC", "trf", "CpG"]:
                s.add(Jobs(chromosome_accession=gca.accession,
                           job_name=job))
            # print(gca.accession, gca.assembly_level, gca.records)
        s.commit()
    else:
        stderr.write("{} was not added because XML record is unavailable\n".format(gca.accession))
    stderr.flush()

# retry download chromosome xml record with a longer timeout
for chromosome in s.query(Chromosome).filter(or_(Chromosome.md5 == None, Chromosome.length == None)).all():
    chrom_xml = xml_download_retry(chromosome.accession)
    if chrom_xml is not None:
        try:
            chromosome.md5, chromosome.length = chromosome_data(chrom_xml)
        except AttributeError:
            stderr.write("Chromosome {} doesn't exit or has corrupted xml file. Chromosome data was not added\n"
                             .format(chromosome.accession))
    s.commit()
    stderr.flush()

s.close()
stderr.close()

