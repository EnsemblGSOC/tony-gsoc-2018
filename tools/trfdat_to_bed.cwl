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
baseCommand: TRFdat_to_bed.py
hints:
  DockerRequirement:
    dockerPull: tonyyzy/trfdat_to_bed_docker
arguments:
  - --bed
  - valueFrom: $(inputs.datfile.nameroot).bed
requirements:
  ResourceRequirement:
    tmpdirMin: 10000
    outdirMin: 10000
    ramMin: 5000
inputs:
  datfile:
    type: File
    inputBinding:
      prefix: --dat
      position: 1

outputs:
  output:
    type: File
    outputBinding:
      glob: "*.bed"
  
