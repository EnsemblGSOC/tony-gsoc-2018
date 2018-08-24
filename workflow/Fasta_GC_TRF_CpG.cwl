# 
# See the NOTICE file distributed with this work for additional information
# regarding copyright ownership.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
  md5script:
    type: File
  
outputs:
  fasta_out:
    type: File
    outputSource: Fasta/output
  GCout:
    type: File
    outputSource: GC/output
  TRF_dat_out:
    type: File
    outputSource: TRF/dat
  TRF_mask_out:
    type: File
    outputSource: TRF/mask
  TRF_bed_out:
    type: File
    outputSource: TRFdat_to_bed/output
  CpG_out:
    type: File
    outputSource: CpG/output
  md5_out:
    type: File
    outputSource: md5/output

steps:
  Fasta:
    run: ../tools/curl-retrieval.cwl
    in:
      accession: accession
      dataformat: dataformat
      seqfile:
        valueFrom: $(inputs.accession).$(inputs.dataformat)
    out: [output]
  
  md5:
    run: ../tools/md5.cwl
    in:
      genomefile: Fasta/output
      md5script: md5script
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
    out: [dat, mask]
  
  TRFdat_to_bed:
    run: ../tools/trfdat_to_bed.cwl
    in:
      datfile:
        source: TRF/dat
    out: [output]
  
  CpG:
    run: ../tools/cpg.cwl
    in:
      accession: accession
      genomefile:
       source: TRF/mask
    out: [output]
    