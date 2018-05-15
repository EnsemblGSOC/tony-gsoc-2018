# tony-gsoc-2018

A CWL workflow to perform automated analysis on genomes.

## Main workflow script - Retrieve_GC_workflow.cwl

Connect curl-retrieval.cwl and python_GC.cwl. This workflow takes an ENA accession number as input and outputs a wiggle file contains GC analysis results.

## curl-retreval.cwl

This script takes an ENA accession number as input, utilises ENA's REST api to find and download genome sequences in FASTA format. Input example is given in *curl-example-input.yml*.

## Python_GC.cwl

A cwl wrapper of *naiveGC.py*. This script takes a fasta formatted nucletotide sequence and outputs calculated GC analysis result in wiggle format. Example input is given in *python_GC.cwl*.

## naiveGC.py

A simple implementation of GC analysis algorithm in Python.
Example usage:
```bash
python naiveGC.py genome_file_in_fasta_format starting_position window_size output_file_name
python naiveGC.py "GRCh38-Chrom17.fasta" 0 5 "GRCh38-Chrom17.wig"

