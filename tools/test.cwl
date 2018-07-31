#!usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
baseCommand: echo

requirements:
  - class: InlineJavascriptRequirement

inputs:
  strings:
    type: string[]
    inputBinding:
      position: 1

outputs: []