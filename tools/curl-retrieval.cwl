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
class: CommandLineTool
baseCommand: curl
hints:
  DockerRequirement:
    dockerPull: sequenceiq/alpine-curl
requirements:
  ResourceRequirement:
    tmpdirMin: 20000
    outdirMin: 20000
arguments:
  - valueFrom: https://www.ebi.ac.uk/ena/data/view/$(inputs.accession)&display=$(inputs.dataformat)
inputs:
  accession:
    type: string
  dataformat:
    type: string
  seqfile:
    type: string
    inputBinding:
      prefix: -o
      valueFrom: $(inputs.accession).$(inputs.dataformat)
outputs:
  output:
    type: File
    outputBinding:
      glob: $(inputs.accession).$(inputs.dataformat)