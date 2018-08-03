#!usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
baseCommand: gzip
arguments:
  - -d
  - -c
requirements:
  ResourceRequirement:
    tmpdirMin: 30000
    outdirMin: 30000
    ramMin: 5000
stdout: $(inputs.gzfile.nameroot)
inputs:
  gzfile:
    type: File
    inputBinding:
      position: 1

outputs:
  output:
    type: File
    outputBinding:
      glob: "*.fasta"
  
