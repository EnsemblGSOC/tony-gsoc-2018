import shutil
import os


def generate_yaml_input(accession):
    workdir = r"/hps/nobackup2/production/ensembl/tony/results/{}".format(accession)
    if not os.path.exists(workdir):
        os.makedirs(workdir)
    workflow_input = open(workdir + "/Fasta_GC_TRF_CpG_{}.yml".format(accession), mode="w")
    workflow_input.write("accession: \"{}\"\n".format(accession))
    shutil.copyfileobj(open("../workflow/Fasta_GC_TRF_CpG_vanilla.yml"), workflow_input)


if __name__ == "__main__":
    accession = "CM000686.2"
    generate_yaml_input(accession)