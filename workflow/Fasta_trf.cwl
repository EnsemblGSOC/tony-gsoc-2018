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
# 

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
    