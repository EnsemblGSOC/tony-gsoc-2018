#!usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
requirements:
  - class: ShellCommandRequirement
baseCommand: 
stdout: $(inputs.genomefile.nameroot).md5
requirements:
  ResourceRequirement:
    tmpdirMin: 20000
    outdirMin: 20000
  EnvVarRequirement:
    envDef:
      PATH: /usr/bin
inputs:
  genomefile:
    type: File
  tail:
    type: string
    default: " "
    inputBinding:
      position: 1
      shellQuote: False
      valueFrom: "tail -n +2 $(inputs.genomefile.path) | tr -d '\n' | md5sum"
outputs:
  output:
    type: stdout
  
