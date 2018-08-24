#!usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
baseCommand: python
hints:
  DockerRequirement:
    dockerPull: tonyyzy/python2.7_requests
inputs:
  script:
    type: File
    inputBinding:
      position: 1
  accession:
    type: string
    inputBinding:
      position: 2
stdout: $(inputs.accession).url
outputs:
  output:
    type: stdout
  
