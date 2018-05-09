#!usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
baseCommand: python
hints:
  DockerRequirement:
    dockerPull: python:3.6.5-alpine3.7
inputs:
  script:
    type: File
    inputBinding:
      position: 1
  genomefile:
    type: File
    inputBinding:
      position: 2
  start:
    type: string
    inputBinding:
      position: 3
  length:
    type: string
    inputBinding:
      position: 4
  outputfile:
    type: string
    inputBinding:
      position: 5
outputs:
  output:
    type: File
    outputBinding:
      glob: $(inputs.outputfile)
  
