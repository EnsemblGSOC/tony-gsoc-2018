# Google Summer of Code 2018 Final Work Product
# Automated Processing of Primary Genome Analysis
Tony Yang (tony@tony.tc)

## Abstract
In this GSoC project, three phased goals were achieved.
* A program to calculate the percentage of guanine and cytosine in genome sequences. ([repository link](https://github.com/tonyyzy/GC_analysis))
* Common Workflow Language (cwl) workflows that perform genome analysis. ([workflows](https://github.com/EnsemblGSOC/tony-gsoc-2018/tree/master/workflow), [commandline tools](https://github.com/EnsemblGSOC/tony-gsoc-2018/tree/master/tools))
* A framework for running workflows on newly reported genome assemblies. ([scripts](https://github.com/EnsemblGSOC/tony-gsoc-2018/tree/master/scripts))

## Introduction
With the development of new sequencing machineries and their much-reduced cost, a large quantity of novel genome data is produced daily at an increasing rate by goverment and private funded genome projects. Hence, it is crucial to perform automated analyses on those data as they are produced.

## What work was done?
I started by writing a GC program in Python, which was the goal of the first phase of this GSoC project. This commandline program would take a fasta formatted file which contains one or more genome sequences, and calculate the GC percentage of a specified window-szie and shift then write the result to file. The output file format can be chosen among wiggle file, gzip compressed wiggle file or bigwig file. The results of multi-sequence input file can be a single file or separated to one sequence per file. This GC program can be executed as a Python script, from the pakcaged binary file, install the package from PYPI or run the docker image as a container. For detailed usage and options, please see the [repository](https://github.com/tonyyzy/GC_analysis).

For the second stage, I containerised my GC program into a docker image, along with several other tools and scripts. I also developed CWL commandline scripts for each of the tools (see [tools](https://github.com/EnsemblGSOC/tony-gsoc-2018/tree/master/tools)) and workflows to run all the analyses by providing an ENA accession number (see [workflows](https://github.com/EnsemblGSOC/tony-gsoc-2018/tree/master/workflow)). These CWL files set the stage for the deployment of the workflow to clusters.

For the final stage, I deployed the workflows to EBI's cluster. My Python [scripts](https://github.com/EnsemblGSOC/tony-gsoc-2018/tree/master/scripts) would retrieve a list of assemblies from a internal data base, which is updated daily, consists the ENA accessions for all the assemblies on ENA's archive. Subsequently, my scripts `Update_tables.py` would update my own MySQL database which holds information about the assemblies and their chromosomes, together with all jobs and their statuses. `submit_jobs.py` will generate the YAML input files for CWL and submit all waiting jobs to LSF with Toil (a CWL executor with batch system support). Finally, `process_result.py` would parse the CWL output and update the jobs' statuses accordingly, then aggregate the result to determine if a whole assembly's jobs are all done.

