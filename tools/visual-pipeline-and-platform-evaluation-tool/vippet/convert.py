import re
from collections import defaultdict
from collections.abc import Iterator, Mapping
from dataclasses import dataclass
from typing import Any

from models import get_supported_models_manager
from videos import get_videos_manager


models_manager = get_supported_models_manager()
videos_manager = get_videos_manager()


@dataclass
class _Token:
    kind: str | None
    value: str


def _tokenize(element: str) -> Iterator[_Token]:
    token_specification = [
        ("PROPERTY", r"\S+\s*=\s*\S+"),  # Property in key=value format
        ("TEE_END", r"\S+\.(?:\s|\Z)"),  # End of tee
        ("TYPE", r"\S+"),  # Element type
        ("SKIP", r"[ \t]+"),  # Skip over spaces and tabs
        ("MISMATCH", r"."),  # Any other character
    ]

    tok_regex = "|".join(
        f"(?P<{name}>{pattern})" for name, pattern in token_specification
    )

    for mo in re.finditer(tok_regex, element):
        kind = mo.lastgroup
        value = mo.group().strip()
        if kind == "SKIP":
            continue
        yield _Token(kind, value)


def _model_path_to_display_name(nodes):
    for node in nodes:
        path = node.get("data", {}).get("model", None)
        if not path:
            continue

        model = models_manager.find_installed_model_by_model_path_full(path)
        # TODO handle case where model is not found by path
        if not model:
            continue

        node["data"]["model"] = model.display_name
        # TODO does model-proc also needs display name?
        if "model-proc" in node["data"]:
            del node["data"]["model-proc"]

    return nodes


def _video_path_to_display_name(nodes):
    for node in nodes:
        for k, v in node["data"].items():
            filename = videos_manager.get_video_filename(v)
            if not filename:
                continue

            node["data"][k] = filename

    return nodes


def string_to_config(launch_string: str) -> Mapping:
    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, str]] = []

    tee_indices: list[str] = []
    prev_token = _Token("", "")

    launch_string = launch_string.replace(",", " ")

    for i, element in enumerate(launch_string.split("!")):
        for token in _tokenize(element):
            match token.kind:
                case "TYPE":
                    nodes.append({"id": str(i), "type": token.value, "data": {}})

                    if i > 0:
                        edges.append(
                            {
                                "id": str(i - 1),
                                "source": (
                                    str(i - 1)
                                    if prev_token.kind != "TEE_END"
                                    else tee_indices.pop()
                                ),
                                "target": str(i),
                            }
                        )

                    if token.value == "tee":
                        tee_indices.append(str(i))

                case "PROPERTY":
                    key, value = re.split(r"\s*=\s*", token.value, maxsplit=1)
                    if nodes:
                        nodes[-1]["data"][key] = value

                case "MISMATCH":  # TODO
                    print(f"MISMATCH: {token}")

            prev_token = token

    nodes = _model_path_to_display_name(nodes)
    nodes = _video_path_to_display_name(nodes)

    return {"nodes": nodes, "edges": edges}


def _model_display_name_to_path(nodes):
    for node in nodes:
        name = node.get("data", {}).get("model", None)
        if not name:
            continue

        model = models_manager.find_installed_model_by_display_name(name)
        # TODO handle case where model is not found by display name
        if not model:
            continue

        node["data"]["model"] = model.model_path_full
        if model.model_proc_full:
            node["data"]["model-proc"] = model.model_proc_full

    return nodes


def _video_name_to_path(nodes):
    for node in nodes:
        for k, v in node["data"].items():
            path = videos_manager.get_video_path(v)
            if not path:
                continue

            node["data"][k] = path

    return nodes


def config_to_string(pipeline: Mapping) -> str:
    nodes = pipeline.get("nodes", [])
    if not nodes:
        return ""

    nodes = _model_display_name_to_path(nodes)
    nodes = _video_name_to_path(nodes)

    edges = pipeline.get("edges", [])
    node_by_id = {node["id"]: node for node in nodes}

    # Build adjacency map for efficient edge lookup
    edges_from: dict[str, list[str]] = defaultdict(list)
    for edge in edges:
        source = edge["source"]
        target = edge["target"]
        edges_from[source].append(target)

    # Find tee elements and their names
    tee_names = {
        node["id"]: node["data"]["name"]
        for node in nodes
        if node["type"] == "tee" and "name" in node["data"]
    }

    # Find start nodes (nodes with no incoming edges)
    all_node_ids = set(node_by_id.keys())
    target_node_ids = set(edge["target"] for edge in edges)
    start_nodes = all_node_ids - target_node_ids

    # TODO log error for circular graphs
    if not start_nodes:
        print("Warning: Circular graph detected or no start nodes found.")
        return ""

    result_parts: list[str] = []
    visited: set[str] = set()

    def build_chain(start_id: str) -> None:
        current_id = start_id

        while current_id and current_id not in visited:
            visited.add(current_id)
            node = node_by_id.get(current_id)
            if not node:
                break

            result_parts.append(node["type"])

            for key, value in node["data"].items():
                result_parts.append(f"{key}={value}")

            targets = edges_from.get(current_id, [])

            if not targets:
                break
            if len(targets) == 1:
                result_parts.append("!")
                current_id = targets[0]
            else:
                result_parts.append("!")
                build_chain(targets[0])

                for target_id in targets[1:]:
                    tee_name = tee_names.get(current_id, "t")
                    result_parts.append(f"{tee_name}.")
                    result_parts.append("!")
                    build_chain(target_id)

                return

    for start_id in sorted(start_nodes):
        if start_id not in visited:
            build_chain(start_id)

    return " ".join(result_parts)
