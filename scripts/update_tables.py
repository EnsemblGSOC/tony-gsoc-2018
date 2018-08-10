from __future__ import print_function
from base import *
from sqlalchemy import create_engine, Table, MetaData, func, or_
from sqlalchemy.orm import sessionmaker
import sys
import requests
import xml.etree.ElementTree as ET
from datetime import datetime
import ast

with open("../../scripts/config.py") as configfile:
    config = ast.literal_eval(configfile.read())

tony_assembly = config["tony_assembly"]
results_dir = config ["results_dir"]
udocker_root = config["udocker_root"]
toil_dir = config["toil_dir"]
workflow_dir = config["workflow_dir"]
log_dir = config["log_dir"]
registry = config["registry"]


def xml_download(ena_accession):
    try:
        xml = ET.fromstring(requests.get("https://www.ebi.ac.uk/ena/data/view/{}&display=xml".format(ena_accession),
                                         stream=True, timeout=60).content)
        return xml
    except requests.exceptions.ReadTimeout:
        stderr.write("Could not download XML file with accession {}\n".format(ena_accession))
        return None


def chromosome_number(xml):
    try:
        chroms_number = len(xml.find("ASSEMBLY").find("CHROMOSOMES").findall("CHROMOSOME"))
        return chroms_number
    except AttributeError:
        return 0


def get_chromosomes(xml):
    for record in xml.find("ASSEMBLY").find("CHROMOSOMES").findall("CHROMOSOME"):
        yield record


def chromosome_data(xml):
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
    if gca_xml is not None:
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

for chromosome in s.query(Chromosome).filter(or_(Chromosome.md5 == None, Chromosome.length == None)).all():
    chrom_xml = xml_download(chromosome.accession)
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

