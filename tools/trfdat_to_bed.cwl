#!usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
baseCommand: TRFdat_to_bed.py
hints:
  DockerRequirement:
    dockerPull: tonyyzy/trfdat_to_bed_docker
arguments:
  - --bed
  - valueFrom: $(inputs.datfile.nameroot).bed
requirements:
  ResourceRequirement:
    tmpdirMin: 10000
    outdirMin: 10000
    ramMin: 5000
inputs:
  datfile:
    type: File
    inputBinding:
      prefix: --dat
      position: 1

outputs:
  output:
    type: File
    outputBinding:
      glob: "*.bed"
  
