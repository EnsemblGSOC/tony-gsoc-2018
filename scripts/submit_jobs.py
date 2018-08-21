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

import ast
import os
import shutil
import subprocess
import sys

from sqlalchemy import create_engine, distinct
from sqlalchemy.orm import sessionmaker

from base import *

config_path = sys.argv[1]

with open(config_path) as configfile:
    config = ast.literal_eval(configfile.read())

tony_assembly = config["tony_assembly"]
results_dir = config ["results_dir"]
udocker_root = config["udocker_root"]
toil_dir = config["toil_dir"]
workflow_dir = config["workflow_dir"]


def generate_yaml_input(accession):
    workdir = r"{results_dir}/{accession}".format(results_dir=results_dir, accession=accession)
    if not os.path.exists(workdir):
        os.makedirs(workdir)
    if accession[0:3] == "GCA":
        workflow_input = open(workdir + "/Gz_Fasta_GC_TRF_CpG_{}.yml".format(accession), mode="w")
        workflow_input.write("accession: \"{}\"\n".format(accession))
        shutil.copyfileobj(open("{workflow_dir}/Gz_Fasta_GC_TRF_CpG_vanilla.yml".format(workflow_dir=workflow_dir)), workflow_input)
    else:
        workflow_input = open(workdir + "/Fasta_GC_TRF_CpG_{}.yml".format(accession), mode="w")
        workflow_input.write("accession: \"{}\"\n".format(accession))
        shutil.copyfileobj(open("{workflow_dir}/Fasta_GC_TRF_CpG_vanilla.yml".format(workflow_dir=workflow_dir)), workflow_input)


if __name__ == "__main__":
    engine = create_engine(tony_assembly)
    session = sessionmaker(bind=engine)
    s = session()
    ena_accessions = [x[0] for x in s.query(distinct(Jobs.chromosome_accession))
                                     .filter(Jobs.status == None).limit(150).all()]
    for ena_accession in ena_accessions:
        generate_yaml_input(ena_accession)
        if ena_accession[0:3] == "GCA":
            subprocess.Popen(
                "export UDOCKER_DIR={udocker_root}/udocker;"
                "export PATH=$PATH:{udocker_root}/bin;"
                "bsub "
                "-e {results_dir}/{accession}/stderr.txt "
                "-o {results_dir}/{accession}/stdout.txt "
                "{toil_dir}/toil-cwl-runner "
                "--batchSystem=lsf "
                "--disableCaching "
                "--logDebug "
                "--logFile={results_dir}/{accession}/log.txt "
                "--jobStore={results_dir}/{accession}/jobstore "
                "--clean=onSuccess "
                "--cleanWorkDir=onSuccess "
                "--user-space-docker-cmd=udocker "
                "--workDir={results_dir}/{accession}/ "
                "--outdir={results_dir}/{accession}/ "
                "{workflow_dir}/Gz_Fasta_GC_TRF_CpG.cwl "
                "{results_dir}/{accession}/Gz_Fasta_GC_TRF_CpG_{accession}.yml"
                .format(udocker_root=udocker_root, results_dir=results_dir, accession=ena_accession,
                        toil_dir=toil_dir, workflow_dir=workflow_dir), shell=True)
        else:
            subprocess.Popen(
                "export UDOCKER_DIR={udocker_root}/udocker;"
                "export PATH=$PATH:{udocker_root}/bin;"
                "bsub "
                "-e {results_dir}/{accession}/stderr.txt "
                "-o {results_dir}/{accession}/stdout.txt "
                "{toil_dir}/toil-cwl-runner "
                "--batchSystem=lsf "
                "--disableCaching "
                "--logDebug "
                "--logFile={results_dir}/{accession}/log.txt "
                "--jobStore={results_dir}/{accession}/jobstore "
                "--clean=onSuccess "
                "--cleanWorkDir=onSuccess "
                "--user-space-docker-cmd=udocker "
                "--workDir={results_dir}/{accession}/ "
                "--outdir={results_dir}/{accession}/ "
                "{workflow_dir}/Fasta_GC_TRF_CpG.cwl "
                "{results_dir}/{accession}/Fasta_GC_TRF_CpG_{accession}.yml"
                .format(udocker_root=udocker_root, results_dir=results_dir, accession=ena_accession,
                        toil_dir=toil_dir, workflow_dir=workflow_dir), shell=True)
        for job in s.query(Jobs).filter(Jobs.chromosome_accession == ena_accession).all():
            job.status = 1
        s.commit()