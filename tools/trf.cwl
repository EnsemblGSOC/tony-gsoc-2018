#!usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
baseCommand: trf
hints:
  DockerRequirement:
    dockerPull: quay.io/biocontainers/trf:4.09--1
inputs:
  genomefile:
    type: File
    inputBinding:
      position: 2
  match:
    type: string
    inputBinding:
      position: 3
  mismatch:
    type: string
    inputBinding:
      position: 4
  delta:
    type: string
    inputBinding:
      position: 5
  PM:
    type: string
    inputBinding:
      position: 6
  PI:
    type: string
    inputBinding:
      position: 7
  minscore:
    type: string
    inputBinding:
      position: 8
  maxperiod:
    type: string
    inputBinding:
      position: 9
    
outputs:
  output:
    type:
      type: array
      items: File
    outputBinding:
      glob: "*.html"
  
