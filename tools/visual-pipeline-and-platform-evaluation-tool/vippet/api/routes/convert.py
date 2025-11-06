from convert import Config, config_to_string, string_to_config
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
    return LaunchConfig.model_validate(response.to_dict())


@router.post(
    "/to-string",
    operation_id="to_string",
    summary="Convert launch config to launch string",
)
def to_string(request: LaunchConfig) -> LaunchString:
    d = request.model_dump()
    response = config_to_string(Config.from_dict(d))
    return LaunchString(launch_string=response)
