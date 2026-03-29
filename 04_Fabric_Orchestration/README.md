# Microsoft Fabric Orchestration

## Objective
This submission demonstrates a Microsoft Fabric pipeline design to orchestrate a batch data processing flow across Bronze, Silver, and Gold notebooks.

## Pipeline design
The orchestration uses a single Fabric pipeline with three notebook activities:

1. NB_Bronze
2. NB_Silver
3. NB_Gold

Execution order:
NB_Bronze -> NB_Silver -> NB_Gold

## Parameters passed between notebooks
The same execution context is passed to all notebooks:

- environment
- run_id
- rerun_mode
- pipeline_start_time
- pipeline_name

`run_id` is generated from the Fabric pipeline run and reused across Bronze, Silver, and Gold.

## Error handling
Each notebook activity has:
- retry count = 3
- retry interval = 30 seconds

Failure branches are included:
- Fail_Bronze
- Fail_Silver
- Fail_Gold

## Environment strategy
The same pipeline design is reusable across:
- dev
- test
- prod

Environment-specific values are controlled using pipeline parameters and config mapping.

## Operational notes
- Bronze runs first
- Silver starts only if Bronze succeeds
- Gold starts only if Silver succeeds
- Failure in any layer stops the pipeline
- Shared run_id supports audit tracing across all layers

## Files included
- pipeline-content.json
- parameter_config.json
- notebook code with parameter handling