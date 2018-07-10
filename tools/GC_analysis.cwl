#!usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
baseCommand: GC_analysis
hints:
  DockerRequirement:
    dockerPull: tonyyzy/gc_analysis
inputs:
  genomefile:
    type: File
    inputBinding:
      prefix: -i
      position: 2
  window_size:
    type: string
    inputBinding:
      prefix: -w
      position: 3
  step:
    type: string
    inputBinding:
      prefix: -s
      position: 4
  outputfile:
    type: string
    inputBinding:
      prefix: -o
      position: 5
  format:
    type: string
    inputBinding:
      prefix: -f
      position: 6
  omittail:
    type: string
    default: null
    inputBinding:
      position: 7
outputs:
  output:
    type: File
    outputBinding:
      glob: $(inputs.outputfile).wig
  
