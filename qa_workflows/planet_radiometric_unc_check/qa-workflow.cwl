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
    label: Planet SuperDove QA radiometric unc test
    doc: Planet SuperDove QA radiometric unc test
    inputs:
      s3_endpoint:
        label: https s3 endpoint
        doc: https s3 endpoint
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
        out:
          - results

  # Main Python script execution
  - class: CommandLineTool
    id: qa-workflow
    hints:
      DockerRequirement:
        dockerPull: docker.io/sm41/qa-workflow-planet
    baseCommand: ["/usr/local/bin/python3", "-m", "qa-workflow"] # or "/venv/bin/python" ?
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