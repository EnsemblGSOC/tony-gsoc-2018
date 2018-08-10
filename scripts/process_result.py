# Copyright 2018 Tony Zeyu Yang
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function
import re
from base import *
from sqlalchemy import create_engine, distinct, func
from sqlalchemy.orm import sessionmaker
import os.path
import shutil
import ast
import subprocess

with open("../../scripts/config.py") as configfile:
    config = ast.literal_eval(configfile.read())

tony_assembly = config["tony_assembly"]
results_dir = config["results_dir"]
engine = create_engine("tony_assembly")
session = sessionmaker(bind=engine)
s = session()


def verify_jobs(file_dict, sql_session, accession):
    GC, trf, CpG, fasta = [None, None, None, None]
    if os.path.isfile("{results_dir}/{accession}/{accession}.fasta.2.5.7.80.10.40.500.bed".format(results_dir=results_dir, accession=accession)) \
            and os.path.isfile("{results_dir}/{accession}/{accession}.fasta.2.5.7.80.10.40.500.mask".format(results_dir=results_dir, accession=accession)) \
            and os.path.isfile("{results_dir}/{accession}/{accession}.fasta.2.5.7.80.10.40.500.dat".format(results_dir=results_dir, accession=accession)):
        trf = 0
    if os.path.isfile("{results_dir}/{accession}/{accession}.wig".format(results_dir=results_dir, accession=accession))\
            and file_dict["GCout"]["size"] > 0:
        GC = 0
    if os.path.isfile("{results_dir}/{accession}/{accession}.CpG.txt".format(results_dir=results_dir, accession=accession)):
        CpG = 0
    if os.path.isfile("{results_dir}/{accession}/{accession}.fasta".format(results_dir=results_dir, accession=accession))\
            and file_dict["fasta_out"]["size"] > 0:
        fasta = 0
    for job in sql_session.query(Jobs).filter(Jobs.chromosome_accession == accession).all():
        if job.job_name == "GC":
            job.status = GC
            job.SHA1 = file_dict["GCout"]["checksum"][5:]
        elif job.job_name == "trf":
            job.status = trf
            job.SHA1 = file_dict["TRF_bed_out"]["checksum"][5:]
        elif job.job_name == "CpG":
            job.status = CpG
            job.SHA1 = file_dict["CpG_out"]["checksum"][5:]
        elif job.job_name == "get_fasta":
            job.status = fasta
            job.SHA1 = file_dict["fasta_out"]["checksum"][5:]
    sql_session.commit()


def reset(accession):
    for job in s.query(Jobs).filter(Jobs.chromosome_accession == accession).all():
        job.status = None
    s.commit()


if __name__ == "__main__":
    # submitted = [x[0] for x in s.query(Jobs).filter(Jobs.status == 1).all()]
    pattern = re.compile(r"\{(\s+)(.+)(\s+)\}", re.DOTALL)
    running_jobs = [x[4:-4] for x in subprocess.check_output(["bjobs -w | grep -o \"CpG_.*.yml\""], shell=True).strip().split("\n")]
    submitted_jobs = [x[0] for x in s.query(distinct(Jobs.chromosome_accession)).filter(Jobs.status == 1).all()]
    finished_jobs = [x for x in submitted_jobs if x not in running_jobs]
    for ena_accession in finished_jobs:
        try:
            match = pattern.findall(open("{results_dir}/{accession}/stdout.txt"
                                         .format(results_dir=results_dir, accession=ena_accession), "r").read())
            if match:  # Result files summary exists
                output_files = ast.literal_eval("{" + "".join(match[-1]) + "}")
                if ena_accession[0:3] == "GCA":
                    verify_jobs(output_files, s, ena_accession)
                else:
                    with open("{results_dir}/{accession}/{accession}.md5"
                               .format(results_dir=results_dir, accession=ena_accession), "r") as md5:
                        if md5.read(32) == \
                                s.query(Chromosome.md5).filter(Chromosome.accession == ena_accession).all()[0][0]:
                            verify_jobs(output_files, s, ena_accession)
                        else:
                            reset(ena_accession)
            else:  # failed job
                reset(ena_accession)
        except Exception as e:
            print(e)
            reset(ena_accession)

    for chromosome_accession in [x[0] for x in
                                 s.query(Jobs.chromosome_accession)
                                         .group_by(Jobs.chromosome_accession)
                                         .having(func.sum(Jobs.status) == 0).all()]:
        if chromosome_accession[:3] == "GCA":
            s.query(GCA).filter(GCA.accession == chromosome_accession).scalar().status = 0
        else:
            for chromosome in s.query(Chromosome).filter(Chromosome.accession == chromosome_accession).all():
                chromosome.status = 0
    s.commit()

    for GCA_accession in [x[0] for x in
                          s.query(Chromosome.GCA_accession)
                                  .group_by(Chromosome.GCA_accession)
                                  .having(func.sum(Chromosome.status) == 0).all()]:
        s.query(GCA).filter(GCA.accession == GCA_accession).scalar().status = 0
        GCAdir = r"{results_dir}/{GCA_accession}".format(results_dir=results_dir, GCA_accession=GCA_accession)
        if not os.path.exists(GCAdir):
            for chromosome in [x[0] for x in
                               s.query(Chromosome.accession).filter(Chromosome.GCA_accession == GCA_accession)]:
                chrom_source = r"{results_dir}/{chromosome}".format(results_dir=results_dir, chromosome=chromosome)
                chrom_destination = r"{results_dir}/{GCA_accession}/{chromosome}".format(results_dir=results_dir,
                                                                                         GCA_accession=GCA_accession,
                                                                                         chromosome=chromosome)
                shutil.copytree(chrom_source, chrom_destination)
    s.commit()
    s.close()
