from hypergraph_db.models import Node, Hyperedge, EmbeddingMetadata


def test_node_creation():
    node = Node(body='{"id": "node1", "name": "Alpha"}')
    assert node.body == '{"id": "node1", "name": "Alpha"}'
    assert node.id is None


def test_hyperedge_creation():
    hyperedge = Hyperedge(edge_id="edge1", properties="{}", nodes='["node1", "node2"]')
    assert hyperedge.id == "edge1"
    assert hyperedge.properties == "{}"
    assert hyperedge.nodes == '["node1", "node2"]'


def test_embedding_metadata_creation():
    metadata = EmbeddingMetadata(
        metadata_id="embed1",
        node_id="node1",
        model="modelA",
        start_idx=0,
        end_idx=512,
        child=None,
    )
    assert metadata.id == "embed1"
    assert metadata.node_id == "node1"
    assert metadata.model == "modelA"
