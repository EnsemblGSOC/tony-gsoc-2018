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
  suppress_html: string
  
outputs:
  fasta_out:
    type: File
    outputSource: Fasta/output
  GCout:
    type: File
    outputSource: GC/output
  TRFout:
    type:
      type: array
      items: File
    outputSource: TRF/output
  CpG_out:
    type: File
    outputSource: CpG/output

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
  
  TRF:
    run: ../tools/trf.cwl
    in:
      genomefile:
        source: Fasta/output
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
      suppress_html: suppress_html
    out: [output]
  
  CpG:
    run: ../tools/cpg.cwl
    in:
      genomefile:
       source: Fasta/output
    out: [output]
    