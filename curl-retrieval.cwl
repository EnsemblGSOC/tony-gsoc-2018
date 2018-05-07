#!usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
baseCommand: curl
hints:
  DockerRequirement:
    dockerPull: sequenceiq/alpine-curl
arguments: ["https://www.ebi.ac.uk/ena/data/view/$(inputs.accession)&range=$(inputs.start)-$(inputs.finish)&display=$(inputs.dataformat)"]
inputs:
  outfile:
    type: string
    inputBinding:
      prefix: -o
      position: 1
outputs:
  output:
    type: File
    outputBinding:
      glob: $(inputs.outfile)