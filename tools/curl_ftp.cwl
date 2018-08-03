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
inputs:
  accession:
    type: string
    inputBinding:
      position: 1
      prefix: -o
      valueFrom: $(inputs.accession).fasta.gz
  url:
    type: File
    inputBinding:
      position: 2
      prefix: -K
outputs:
  output:
    type: File
    outputBinding:
      glob: $(inputs.accession).fasta.gz