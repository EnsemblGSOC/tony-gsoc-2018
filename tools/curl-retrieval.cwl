#!usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
baseCommand: curl
hints:
  DockerRequirement:
    dockerPull: sequenceiq/alpine-curl
# arguments: ["https://www.ebi.ac.uk/ena/data/view/$(inputs.accession)&display=$(inputs.dataformat)"]
inputs:
  url:
    type: string
    inputBinding:
      position: 1
    
  seqfile:
    type: string
    inputBinding:
      prefix: -o
      position: 2
outputs:
  output:
    type: File
    outputBinding:
      glob: $(inputs.seqfile)