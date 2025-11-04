import re
from collections import defaultdict
from collections.abc import Iterator, Mapping
from dataclasses import dataclass
from typing import Any


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
                    k, v = re.split(r"\s*=\s*", token.value, maxsplit=1)
                    if nodes:
                        nodes[-1]["data"][k] = v

                case "MISMATCH":  # TODO
                    print(f"MISMATCH: {token}")

            prev_token = token

    return {"nodes": nodes, "edges": edges}


def config_to_string(pipeline: Mapping) -> str:
    nodes = pipeline.get("nodes", [])
    if not nodes:
        return ""

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
    target_node_ids = {edge["target"] for edge in edges}
    start_nodes = all_node_ids - target_node_ids

    # TODO log error for circular graphs
    if not start_nodes:
        print(
            "Warning: Circular graph detected or no start nodes found. Starting from the first node."
        )
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
