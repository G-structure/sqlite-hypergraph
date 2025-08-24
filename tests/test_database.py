import pytest
from hypergraph_db import HypergraphDB, Node, Hyperedge, EmbeddingMetadata


@pytest.fixture
def db():
    db = HypergraphDB(":memory:")
    yield db
    db.close()


def test_insert_node(db):
    node = Node(body='{"id": "node1", "name": "Alpha"}')
    inserted_node = db.insert_node(node)
    assert inserted_node.id == "node1"


def test_insert_hyperedge(db):
    hyperedge = Hyperedge(
        edge_id="edge1", properties='{"weight":1}', nodes='["node1", "node2"]'
    )
    db.insert_hyperedge(hyperedge)
    result = db.connection.execute(
        "SELECT * FROM hyperedges WHERE id = ?", (hyperedge.id,)
    ).fetchone()
    assert result is not None
    assert result["id"] == hyperedge.id


def test_insert_embedding(db):
    node = Node(body='{"id": "node1", "name": "Alpha"}')
    db.insert_node(node)

    embedding_metadata = EmbeddingMetadata(
        metadata_id="embed1",
        node_id=node.id,
        model="all-MiniLM-L6-v2",
        start_idx=0,
        end_idx=512,
        child=None,
    )
    db.insert_embedding(embedding_metadata, node.body)

    result = db.connection.execute(
        "SELECT * FROM embedding_metadata WHERE id = ?", (embedding_metadata.id,)
    ).fetchone()
    assert result is not None
    assert result["node_id"] == node.id


def test_traverse_hypergraph(db):
    # Setup nodes and hyperedges
    node1 = Node(body='{"id": "node1", "name": "Alpha"}')
    node2 = Node(body='{"id": "node2", "name": "Beta"}')
    db.insert_node(node1)
    db.insert_node(node2)

    hyperedge = Hyperedge(edge_id="edge1", properties="{}", nodes='["node1", "node2"]')
    db.insert_hyperedge(hyperedge)
    db.insert_node_hyperedge_map("edge1", "node1", 1)
    db.insert_node_hyperedge_map("edge1", "node2", 2)

    traversal = db.traverse_hypergraph("node1")
    assert len(traversal) > 0


def test_search_hyperedges_multiple_nodes(db):
    node_ids = ["node1", "node2", "node3"]
    nodes = [Node(body=f"{{\"id\": \"{nid}\"}}") for nid in node_ids]
    for node in nodes:
        db.insert_node(node)

    hyperedge = Hyperedge(
        edge_id="edge_multi",
        properties="{}",
        nodes=str(node_ids).replace("'", '"'),
    )
    db.insert_hyperedge(hyperedge)
    for order, nid in enumerate(node_ids, 1):
        db.insert_node_hyperedge_map("edge_multi", nid, order)

    results = db.search_hyperedges(node_ids)
    assert any(row["hyperedge_id"] == "edge_multi" for row in results)
