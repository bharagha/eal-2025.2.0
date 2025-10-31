import re
from collections.abc import Iterator, Mapping
from dataclasses import dataclass


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

    tok_regex = "|".join("(?P<%s>%s)" % pair for pair in token_specification)

    for mo in re.finditer(tok_regex, element):
        kind = mo.lastgroup
        value = mo.group().strip()
        if kind == "SKIP":
            continue
        yield _Token(kind, value)


def string_to_config(launch_string: str) -> Mapping:
    result = {
        "nodes": [],
        "edges": [],
    }

    tee_indices = []
    prev_node = {"id": "", "data": {}}
    prev_token = _Token("", "")

    launch_string = launch_string.replace(",", " ")

    for i, element in enumerate(launch_string.split("!")):
        for token in _tokenize(element):
            match token.kind:
                case "TYPE":
                    result["nodes"].append(
                        {"id": str(i), "type": token.value, "data": {}}
                    )

                    if i > 0:
                        result["edges"].append(
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
                    prev_node["data"][k] = v

                case "MISMATCH":  # TODO
                    print(f"MISMATCH: {token}")

            # TODO This line will raise an IndexError if no nodes have been added yet.
            # The code assumes result["nodes"] is non-empty, but this may not be true depending on the input.
            prev_node = result["nodes"][-1]
            prev_token = token

    return result


def config_to_string(pipeline: Mapping) -> str:
    nodes = pipeline.get("nodes", [])
    if not nodes:
        return ""

    edges = pipeline.get("edges", [])

    # Build adjacency map for efficient edge lookup
    edges_from: dict[str, list[str]] = {}
    for edge in edges:
        source = edge["source"]
        target = edge["target"]
        if source not in edges_from:
            edges_from[source] = []
        edges_from[source].append(target)

    # Find tee elements and their names
    tee_names: dict[str, str] = {}
    for node in nodes:
        if node["type"] == "tee" and "name" in node["data"]:
            tee_names[node["id"]] = node["data"]["name"]

    # Find start nodes (nodes with no incoming edges)
    all_node_ids = {node["id"] for node in nodes}
    target_node_ids = {edge["target"] for edge in edges}
    start_nodes = all_node_ids - target_node_ids

    # TODO log error for circular graphs
    # If no start nodes found (circular graph), pick the first node
    if not start_nodes:
        start_nodes = {nodes[0]["id"]}

    result_parts = []
    visited = set()

    def build_chain(start_id: str) -> None:
        current_id = start_id

        while current_id and current_id not in visited:
            visited.add(current_id)
            node = next((n for n in nodes if n["id"] == current_id), None)
            if not node:
                break

            # Add element type
            result_parts.append(node["type"])

            # Add properties
            for key, value in node["data"].items():
                result_parts.append(f"{key}={value}")

            # Get outgoing edges
            targets = edges_from.get(current_id, [])

            if not targets:
                break
            elif len(targets) == 1:
                result_parts.append("!")
                current_id = targets[0]
            else:
                # Tee element with multiple branches
                result_parts.append("!")
                # Process first branch inline
                build_chain(targets[0])

                # Process remaining branches with tee reference
                for target_id in targets[1:]:
                    tee_name = tee_names.get(current_id, "t")
                    result_parts.append(f"{tee_name}.")
                    result_parts.append("!")
                    build_chain(target_id)

                return

    # Process all connected components
    for start_id in sorted(start_nodes):
        if start_id not in visited:
            build_chain(start_id)

    return " ".join(result_parts)
