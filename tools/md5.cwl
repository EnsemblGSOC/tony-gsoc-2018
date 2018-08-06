#!usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
requirements:
  - class: ShellCommandRequirement
baseCommand: bash
stdout: $(inputs.genomefile.nameroot).md5
requirements:
  ResourceRequirement:
    tmpdirMin: 20000
    outdirMin: 20000

inputs:
  md5script:
    type: File
    inputBinding:
      position: 1
  genomefile:
    type: File
    inputBinding:
      position: 2

outputs:
  output:
    type: stdout
  
