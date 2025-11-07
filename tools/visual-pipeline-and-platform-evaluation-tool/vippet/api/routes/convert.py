from graph import Graph
from fastapi import APIRouter

from api.api_schemas import PipelineGraph, PipelineDescription

router = APIRouter()


@router.post(
    "/to-graph",
    operation_id="to_graph",
    summary="Convert pipeline description to pipeline graph",
)
def to_graph(request: PipelineDescription) -> PipelineGraph:
    graph = Graph.from_pipeline_description(request.pipeline_description)
    return PipelineGraph.model_validate(graph.to_dict())


@router.post(
    "/to-description",
    operation_id="to_description",
    summary="Convert pipeline graph to pipeline description",
)
def to_description(request: PipelineGraph) -> PipelineDescription:
    graph = Graph.from_dict(request.model_dump())
    pipeline_description = graph.to_pipeline_description()
    return PipelineDescription(pipeline_description=pipeline_description)
