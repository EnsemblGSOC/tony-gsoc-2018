#!usr/bin/env cwl-runner

cwlVersion: v1.0
class: Workflow
inputs:
  url: string
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
      url: url
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
    