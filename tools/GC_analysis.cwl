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
      position: 1
  window_size:
    type: string
    inputBinding:
      prefix: -w
      position: 2
  step:
    type: string
    inputBinding:
      prefix: -s
      position: 3
  outputfile:
    type: string
    inputBinding:
      prefix: -o
      position: 4
  omittail:
    type: string
    default: null
    inputBinding:
      position: 6
  outformat:
    type: string
    inputBinding:
      prefix: -f
      position: 5
outputs:
  output:
    type: File
    outputBinding:
      glob: $(inputs.outputfile).wig
  
