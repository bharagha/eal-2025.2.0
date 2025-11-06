from convert import Graph
from fastapi import APIRouter

from api.api_schemas import PipelineGraph, PipelineDescription

router = APIRouter()


@router.post(
    "/to-graph",
    operation_id="to_graph",
    summary="Convert pipeline description to pipeline graph",
)
def to_graph(request: PipelineDescription) -> PipelineGraph:
    response = Graph.from_pipeline_description(request.pipeline_description)
    return PipelineGraph.model_validate(response.to_dict())


@router.post(
    "/to-description",
    operation_id="to_description",
    summary="Convert pipeline graph to pipeline description",
)
def to_description(request: PipelineGraph) -> PipelineDescription:
    d = request.model_dump()
    response = Graph.from_dict(d).to_pipeline_description()
    return PipelineDescription(pipeline_description=response)
