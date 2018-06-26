#!usr/bin/env cwl-runner

cwlVersion: v1.0
class: Workflow
inputs:
  accession: string
  dataformat: string
  seqfile: string
  outputfile: string
  window_size: string
  step: string
  format: string
  
outputs:
  wigout:
    type: File
    outputSource: GC/output

steps:
  download:
    run: ../tools/curl-retrieval.cwl
    in:
      accession: accession
      dataformat: dataformat
      seqfile: seqfile
    out: [output]
  
  GC:
    run: ../tools/GC_analysis.cwl
    in:
      genomefile: download/output
      window_size: window_size
      step: step
      format: format
      outputfile: outputfile
    out: [output]
    