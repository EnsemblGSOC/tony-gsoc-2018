#!usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
baseCommand: /nfs/software/ensembl/RHEL7-JUL2017-core2/pyenv/versions/tony_cwltool/bin/python
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
  