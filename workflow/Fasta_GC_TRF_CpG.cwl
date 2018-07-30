#!usr/bin/env cwl-runner

cwlVersion: v1.0
class: Workflow
requirements:
  - class: StepInputExpressionRequirement
inputs:
  accession: string
  dataformat: string
  window_size: string
  step: string
  outformat: string
  omittail:
    type: string
    default: null
  singlefile:
    type: string
    default: null
    
  
outputs:
  fasta_out:
    type: File
    outputSource: Fasta/output
  GCout:
    type: File
    outputSource: GC/output

steps:
  Fasta:
    run: ../tools/curl-retrieval.cwl
    in:
      accession: accession
      dataformat: dataformat
      seqfile:
        valueFrom: $(inputs.accession).$(inputs.dataformat)
    out: [output]
  
  GC:
    run: ../tools/GC_analysis.cwl
    in:
      genomefile:
        source: Fasta/output
      window_size: window_size
      step: step
      outformat: outformat
      outputfile: accession
      omittail: omittail
      singlefile: singlefile
    out: [output]
    