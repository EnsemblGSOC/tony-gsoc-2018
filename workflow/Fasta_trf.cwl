#!usr/bin/env cwl-runner

cwlVersion: v1.0
class: Workflow
inputs:
  url: string
  seqfile: string
  match: string
  mismatch: string
  delta: string
  PM: string
  PI: string
  minscore: string
  maxperiod: string
  flanking_sequence: string
  data_file: string
  masked_sequence: string
  
outputs:
  intout:
    type: File
    outputSource: download/output
  dataout:
    type:
      type: array
      items: File
    outputSource: trf/output

steps:
  download:
    run: ../tools/curl-retrieval.cwl
    in:
      url: url
      seqfile: seqfile
    out: [output]
  
  trf:
    run: ../tools/trf.cwl
    in:
      genomefile: download/output
      match: match
      mismatch: mismatch
      delta: delta
      PM: PM
      PI: PI
      minscore: minscore
      maxperiod: maxperiod
      flanking_sequence: flanking_sequence
      data_file: data_file
      masked_sequence: masked_sequence
    out: [output]
    