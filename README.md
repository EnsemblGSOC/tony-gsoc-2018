# tony-gsoc-2018

A CWL workflow that retrieves genomic sequence from ENA archive then calculates the GC percentage and writes to output file.

## Main workflow script - Retrieve_GC_workflow.cwl

Connect curl-retrieval.cwl and GC_analysis.cwl. This workflow takes an ENA accession number as input and outputs an output file (wiggle, gzip compressed wiggle or bigwig) contains GC analysis results.

## curl-retreval.cwl

This script takes an ENA accession number as input, utilises ENA's REST api to find and download genome sequences in FASTA format. Input example is given in *curl-example-input.yml*.

## Python_GC.cwl

A cwl wrapper of [*GC_analysis*](https://github.com/tonyyzy/GC_analysis). This script takes a fasta formatted nucletotide sequence and outputs calculated GC analysis result. Example input is given in *GC_analysis.cwl*.

## GC_analysis.py

An implementation of GC analysis algorithm in Python. This project is now hosted under https://github.com/tonyyzy/GC_analysis

