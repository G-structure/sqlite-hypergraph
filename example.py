from hypergraph_db import HypergraphDB, Node, Hyperedge, EmbeddingMetadata

# Initialize the database
db = HypergraphDB("mydatabase.db")

# Insert a node
node = Node(body='{"id": "node1", "name": "Alpha"}')
db.insert_node(node)

# Generate and insert embedding for the node's content
embedding_metadata = EmbeddingMetadata(
    metadata_id="embed1",
    node_id=node.id,
    model="all-MiniLM-L6-v2",
    start_idx=0,
    end_idx=len(node.body),
)
db.insert_embedding(embedding_metadata, node.body)

# Search for similar embeddings
results = db.search_embeddings(query_text="Alpha node", top_k=5)
for result in results:
    print(result)

# Close the database connection
db.close()
