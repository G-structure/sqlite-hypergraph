from typing import Optional

class Node:
    def __init__(self, body: str, node_id: Optional[str] = None):
        self.id = node_id
        self.body = body

    def to_dict(self):
        return {"id": self.id, "body": self.body}


class Hyperedge:
    def __init__(self, edge_id: str, properties: str, nodes: str):
        self.id = edge_id
        self.properties = properties
        self.nodes = nodes

    def to_dict(self):
        return {
            "id": self.id,
            "properties": self.properties,
            "nodes": self.nodes,
        }


class EmbeddingMetadata:
    def __init__(
        self,
        metadata_id: str,
        node_id: str,
        model: str,
        start_idx: int,
        end_idx: int,
        child: Optional[str] = None,
        embedding_id: Optional[int] = None,
    ):
        self.embedding_id = embedding_id
        self.id = metadata_id
        self.node_id = node_id
        self.model = model
        self.start_idx = start_idx
        self.end_idx = end_idx
        self.child = child

    def to_dict(self):
        return {
            "id": self.id,
            "node_id": self.node_id,
            "embedding_id": self.embedding_id,
            "model": self.model,
            "start_idx": self.start_idx,
            "end_idx": self.end_idx,
            "child": self.child,
        }
