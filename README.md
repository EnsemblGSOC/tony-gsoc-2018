# Google Summer of Code 2018 Final Work Product
# Automated Processing of Primary Genome Analysis
Tony Yang (tony@tony.tc)

## Abstract
In this GSoC project, three phased goals were achieved.
* A program to calculate the percentage of guanine and cytosine in genome sequences. ([repository link](https://github.com/tonyyzy/GC_analysis>))
* Common Workflow Language (cwl) workflows that perform genome analysis. ([workflows](https://github.com/EnsemblGSOC/tony-gsoc-2018/tree/master/workflow), [commandline tools](https://github.com/EnsemblGSOC/tony-gsoc-2018/tree/master/tools))
* A framework for running workflows on newly reported genome assemblies. ([scripts](https://github.com/EnsemblGSOC/tony-gsoc-2018/tree/master/scripts))

## Introduction

## Main workflow script - Retrieve_GC_workflow.cwl

Connect curl-retrieval.cwl and GC_analysis.cwl. This workflow takes an ENA accession number as input and outputs an output file (wiggle, gzip compressed wiggle or bigwig) contains GC analysis results.

## curl-retreval.cwl

This script takes an ENA accession number as input, utilises ENA's REST api to find and download genome sequences in FASTA format. Input example is given in *curl-example-input.yml*.

## Python_GC.cwl

A cwl wrapper of [*GC_analysis*](https://github.com/tonyyzy/GC_analysis). This script takes a fasta formatted nucletotide sequence and outputs calculated GC analysis result. Example input is given in *GC_analysis.cwl*.

## GC_analysis.py

An implementation of GC analysis algorithm in Python. This project is now hosted under https://github.com/tonyyzy/GC_analysis

