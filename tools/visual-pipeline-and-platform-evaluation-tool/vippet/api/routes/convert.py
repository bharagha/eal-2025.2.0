from convert import config_to_string, string_to_config
from fastapi import APIRouter

from api.api_schemas import LaunchConfig, LaunchString

router = APIRouter()


@router.post(
    "/to-config",
    operation_id="to_config",
    summary="Convert launch string to launch config",
)
def to_config(request: LaunchString) -> LaunchConfig:
    response = string_to_config(request.launch_string)

    return LaunchConfig(
        nodes=response["nodes"],
        edges=response["edges"],
    )


@router.post(
    "/to-string",
    operation_id="to_string",
    summary="Convert launch config to launch string",
)
def to_string(request: LaunchConfig) -> LaunchString:
    response = config_to_string(request.model_dump())

    return LaunchString(launch_string=response)
