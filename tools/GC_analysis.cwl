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
baseCommand: GC_analysis
hints:
  DockerRequirement:
    dockerPull: tonyyzy/gc_analysis
requirements:
  ResourceRequirement:
    tmpdirMin: 50000
    outdirMin: 50000
    ramMin: 16000
inputs:
  genomefile:
    type: File
    inputBinding:
      prefix: -i
      position: 1
  window_size:
    type: string
    inputBinding:
      prefix: -w
      position: 2
  step:
    type: string
    inputBinding:
      prefix: -s
      position: 3
  outputfile:
    type: string
    inputBinding:
      prefix: -o
      position: 4
  omittail:
    type: string
    default: null
    inputBinding:
      position: 5
  outformat:
    type: string
    inputBinding:
      prefix: -f
      position: 6
  singlefile:
    type: string
    default: null
    inputBinding:
      position: 7
outputs:
  output:
    type: File
    outputBinding:
      glob: $(inputs.outputfile).*
  
