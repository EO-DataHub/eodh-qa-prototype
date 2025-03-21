cwlVersion: v1.0
$namespaces:
  s: https://schema.org/
s:softwareVersion: 0.1.2
schemas:
  - http://schema.org/version/9.0/schemaorg-current-http.rdf
$graph:
  # Workflow entrypoint
  - class: Workflow
    id: qa-workflow-radiometric-unc
    label: Planet SuperDove QA radiometric unc test
    doc: Planet SuperDove QA radiometric unc test
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
    outputs:
      - id: results
        type: Directory
        outputSource:
          - qa-workflow-radiometric-unc/results
    steps:
      qa-workflow:
        run: "#qa-workflow-radiometric-unc"
        in:
          s3_endpoint: s3_endpoint
          date_range: date_range
          data_collection: data_collection
        out:
          - results

  # Main Python script execution
  - class: CommandLineTool
    id: qa-workflow-radiometric-unc
    hints:
      DockerRequirement:
        dockerPull: docker.io/sm41/qa-workflow-radiometric-unc
    baseCommand: ["/usr/local/bin/python3", "-m", "qa-workflow-radiometric-unc"] # or "/venv/bin/python" ?
    inputs:
      s3_endpoint:
        type: string
        inputBinding:
          position: 1
      date_range:
        type: string
        inputBinding:
          position: 2
      data_collection:
        type: string
        inputBinding:
          position: 3
    outputs:
      results:
        type: Directory
        outputBinding:
          glob: .