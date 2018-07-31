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
      position: 1
  match:
    type: string
    inputBinding:
      position: 2
  mismatch:
    type: string
    inputBinding:
      position: 3
  delta:
    type: string
    inputBinding:
      position: 4
  PM:
    type: string
    inputBinding:
      position: 5
  PI:
    type: string
    inputBinding:
      position: 6
  minscore:
    type: string
    inputBinding:
      position: 7
  maxperiod:
    type: string
    inputBinding:
      position: 8
  flanking_sequence:
    type: string
    default: null
    inputBinding:
      position: 9
  data_file:
    type: string
    default: null
    inputBinding:
      position: 10
  masked_sequence:
    type: string
    default: null
    inputBinding:
      position: 11
  suppress_html:
    type: string
    inputBinding:
      position: 12
    
outputs:
  dat:
    type: File
    outputBinding:
      glob: "*.dat"
  mask:
    type: File
    outputBinding:
      glob: "*.mask"
  
