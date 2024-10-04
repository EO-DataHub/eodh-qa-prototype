cwlVersion: v1.0
$namespaces:
  s: https://schema.org/
s:softwareVersion: 0.1.2
schemas:
  - http://schema.org/version/9.0/schemaorg-current-http.rdf
$graph:
  # Workflow entrypoint
  - class: Workflow
    id: qa-workflow-test
    label: QA doc review test
    doc: QA doc review test
    inputs:
      s3_endpoint:
        label: https s3 endpoint
        doc: https s3 endpoint
        type: string
    outputs:
      - id: results
        type: Directory
        outputSource:
          - qa-workflow-test/results
    steps:
      qa-workflow-test:
        run: "#run"
        in:
          s3_endpoint: s3_endpoint
        out:
          - results

  # Main Python script execution
  - class: CommandLineTool
    id: run
    hints:
      DockerRequirement:
        dockerPull: docker.io/sm41/qa-workflow-test5:latest
    baseCommand: ["python", "/app/qa-workflow-test"]
    inputs:
      s3_endpoint:
        type: string
        inputBinding:
          position: 1
    outputs:
      results:
        type: Directory
        outputBinding:
          glob: .