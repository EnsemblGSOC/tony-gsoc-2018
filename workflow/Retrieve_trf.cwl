#!usr/bin/env cwl-runner

cwlVersion: v1.0
class: Workflow
inputs:
  accession: string
  dataformat: string
  seqfile: string
  match: string
  mismatch: string
  delta: string
  PM: string
  PI: string
  minscore: string
  maxperiod: string
  
  
  
  
outputs:
  dataout:
    type:
      type: array
      items: File
    outputSource: trf/output

steps:
  download:
    run: ../tools/curl-retrieval.cwl
    in:
      accession: accession
      dataformat: dataformat
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
    out: [output]
    