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
  outformat: string
  omittail:
    type: string
    default: null
  
  
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
      outformat: outformat
      outputfile: outputfile
      omittail: omittail
    out: [output]
    