#!usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
baseCommand: gzip
arguments:
  - -d
  - -c

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
  
