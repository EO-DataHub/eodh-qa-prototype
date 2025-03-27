cwlVersion: v1.0
$namespaces:
  s: https://schema.org/
s:softwareVersion: 0.1.2
schemas:
  - http://schema.org/version/9.0/schemaorg-current-http.rdf
$graph:
  # Workflow entrypoint
  - class: Workflow
    id: qa-workflow
    label: QA workflow
    doc: QA workflow
    inputs:
      s3_endpoint:
        label: https s3 endpoint
        doc: https s3 endpoint
        type: string
      date_range:
        label: date range for checks
        doc: date range for checks
        type: string
      data_collection:
        label: data collection tested
        doc: data collection tested
        type: string
      qa_check_type:
        label: type of qa check
        doc: type of qa check
        type: string
    outputs:
      - id: results
        type: Directory
        outputSource:
          - qa-workflow/results
    steps:
      qa-workflow:
        run: "#qa-workflow"
        in:
          s3_endpoint: s3_endpoint
          date_range: date_range
          data_collection: data_collection
          qa_check_type: qa_check_type
        out:
          - results

  # Main Python script execution
  - class: CommandLineTool
    id: qa-workflow
    hints:
      DockerRequirement:
        dockerPull: docker.io/sm41/qa-workflow:latest
    baseCommand: ["/usr/local/bin/python3", "-m", "qa-workflow"]
    inputs:
      s3_endpoint:
        type: string
        inputBinding:
          position: 1
      qa_check_type:
        type: string
        inputBinding:
          position: 2
      date_range:
        type: string
        inputBinding:
          position: 3
      data_collection:
        type: string
        inputBinding:
          position: 4
    outputs:
      results:
        type: Directory
        outputBinding:
          glob: .