#!usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
baseCommand: cpglh
hints:
  DockerRequirement:
    dockerPull: tonyyzy/cpg_island_docker
stdout: $(inputs.accession).CpG.txt
inputs:
  accession:
    type: string
  genomefile:
    type: File
    inputBinding:
      position: 1

outputs:
  output:
    type: stdout
  
