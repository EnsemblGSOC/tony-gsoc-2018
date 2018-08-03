import shutil
import os
from base import *
from sqlalchemy import create_engine, distinct, MetaData, func, or_
from sqlalchemy.orm import sessionmaker
import subprocess


def generate_yaml_input(accession):
    workdir = r"/hps/nobackup2/production/ensembl/tony/results/{}".format(accession)
    if os.path.exists(workdir):
        shutil.rmtree(workdir)
    os.makedirs(workdir)
    if accession[0:3] == "GCA":
        workflow_input = open(workdir + "/Gz_Fasta_GC_TRF_CpG_{}.yml".format(accession), mode="w")
        workflow_input.write("accession: \"{}\"\n".format(accession))
        shutil.copyfileobj(open("/hps/nobackup2/production/ensembl/tony/tony-gsoc-2018"
                                "/workflow/Gz_Fasta_GC_TRF_CpG_vanilla.yml"), workflow_input)
    else:
        workflow_input = open(workdir + "/Fasta_GC_TRF_CpG_{}.yml".format(accession), mode="w")
        workflow_input.write("accession: \"{}\"\n".format(accession))
        shutil.copyfileobj(open("/hps/nobackup2/production/ensembl/tony/tony-gsoc-2018"
                                "/workflow/Fasta_GC_TRF_CpG_vanilla.yml"), workflow_input)


if __name__ == "__main__":
    engine = create_engine("mysql://ensadmin:ensembl@mysql-ens-genebuild-prod-7.ebi.ac.uk:4533/tony_assembly")
    session = sessionmaker(bind=engine)
    s = session()
    ena_accessions = [x[0] for x in s.query(distinct(Jobs.chromosome_accession))
                                     .filter(Jobs.status == None).limit(10).all()]
    for ena_accession in ena_accessions:
        generate_yaml_input(ena_accession)
        if ena_accession[0:3] == "GCA":
            subprocess.Popen(
                "export UDOCKER_DIR=/hps/nobackup2/production/ensembl/tony/cwl-udocker-tests/udocker;"
                "export PATH=$PATH:/hps/nobackup2/production/ensembl/tony/cwl-udocker-tests/bin;"
                "bsub "
                "-e /hps/nobackup2/production/ensembl/tony/results/{accession}/stderr.txt "
                "-o /hps/nobackup2/production/ensembl/tony/results/{accession}/stdout.txt "
                "/nfs/software/ensembl/RHEL7-JUL2017-core2/pyenv/versions/toil/bin/toil-cwl-runner "
                "--batchSystem=lsf "
                "--disableCaching "
                "--logDebug "
                "--logFile=/hps/nobackup2/production/ensembl/tony/results/{accession}/log.txt "
                "--jobStore=/hps/nobackup2/production/ensembl/tony/results/{accession}/jobstore "
                "--clean=always "
                "--cleanWorkDir=always "
                "--user-space-docker-cmd=udocker "
                "--workDir=/hps/nobackup2/production/ensembl/tony/results/{accession}/ "
                "--outdir=/hps/nobackup2/production/ensembl/tony/results/{accession}/ "
                "/hps/nobackup2/production/ensembl/tony/tony-gsoc-2018/workflow/Gz_Fasta_GC_TRF_CpG.cwl "
                "/hps/nobackup2/production/ensembl/tony/results/{accession}/Gz_Fasta_GC_TRF_CpG_{accession}.yml"
                .format(accession=ena_accession), shell=True)
        else:
            subprocess.Popen(
                "export UDOCKER_DIR=/hps/nobackup2/production/ensembl/tony/cwl-udocker-tests/udocker;"
                "export PATH=$PATH:/hps/nobackup2/production/ensembl/tony/cwl-udocker-tests/bin;"
                "bsub "
                "-e /hps/nobackup2/production/ensembl/tony/results/{accession}/stderr.txt "
                "-o /hps/nobackup2/production/ensembl/tony/results/{accession}/stdout.txt "
                "/nfs/software/ensembl/RHEL7-JUL2017-core2/pyenv/versions/toil/bin/toil-cwl-runner "
                "--batchSystem=lsf "
                "--disableCaching "
                "--logDebug "
                "--logFile=/hps/nobackup2/production/ensembl/tony/results/{accession}/log.txt "
                "--jobStore=/hps/nobackup2/production/ensembl/tony/results/{accession}/jobstore "
                "--clean=always "
                "--cleanWorkDir=always "
                "--user-space-docker-cmd=udocker "
                "--workDir=/hps/nobackup2/production/ensembl/tony/results/{accession}/ "
                "--outdir=/hps/nobackup2/production/ensembl/tony/results/{accession}/ "
                "/hps/nobackup2/production/ensembl/tony/tony-gsoc-2018/workflow/Fasta_GC_TRF_CpG.cwl "
                "/hps/nobackup2/production/ensembl/tony/results/{accession}/Fasta_GC_TRF_CpG_{accession}.yml"
                    .format(accession=ena_accession), shell=True)
        for job in s.query(Jobs).filter(Jobs.chromosome_accession == ena_accession).all():
            job.status = 1
        s.commit()