#!usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
baseCommand: curl
hints:
  DockerRequirement:
    dockerPull: sequenceiq/alpine-curl
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