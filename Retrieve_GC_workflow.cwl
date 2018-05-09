#!usr/bin/env cwl-runner

cwlVersion: v1.0
class: Workflow
inputs:
  accession: string
  dataformat: string
  start: string
  finish: string
  outfile: string
#  position: string
  
  script: File
  length: string
  outputfile: string
  
outputs:
  wigout:
    type: File
    outputSource: GC/output

steps:
  download:
    run: curl-retrieval.cwl
    in:
      accession: accession
      dataformat: dataformat
      start: start
      finish: finish
      outfile: outfile
    out: [output]
  
  GC:
    run: python_GC.cwl
    in:
      script: script
      genomefile: download/output
      start: start
      length: length
      outputfile: outputfile
    out: [output]
    