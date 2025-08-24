# Hypergraph DB API

A Python API for managing a temporal directed hypergraph SQLite database with text embeddings. It uses `sqlite-vec` for vector search and `sqlite-lembed` for generating embeddings. The API handles complex graph data, including nodes, hyperedges, and embeddings, while enabling vector similarity searches and batch operations for efficiency.

## Key Features

- **Nodes**: Represent entities or objects in the hypergraph. Stored as JSON objects.
- **Hyperedges**: Connect multiple nodes with direction and store additional properties.
- **Embeddings**: Store vector embeddings of node content for semantic searches.
- **Batch Operations**: Insert multiple embeddings or nodes in a single transaction.
- **Text Embedding Generation**: Uses `sqlite-lembed` to generate embeddings from text.
- **Vector Search**: Leverages `sqlite-vec` for efficient nearest‑neighbor searches.
- **Hypergraph Traversal**: Traverse the hypergraph from any starting node, exploring connected edges and nodes.

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
  - [Initializing the Database](#initializing-the-database)
  - [Inserting Nodes and Hyperedges](#inserting-nodes-and-hyperedges)
  - [Inserting Embeddings](#inserting-embeddings)
  - [Batch Inserting Embeddings](#batch-inserting-embeddings)
  - [Searching Nodes](#searching-nodes)
  - [Performing Vector Search](#performing-vector-search)
  - [Hypergraph Traversal](#hypergraph-traversal)
  - [Closing the Database Connection](#closing-the-database-connection)
- [Running Tests](#running-tests)
- [Contributing](#contributing)
- [License](#license)
- [Summary](#summary)

## Requirements

- Python 3.10+
- SQLite 3.31.0+ (for JSON and virtual table support)
- `sqlite-vec` and `sqlite-lembed` SQLite extensions
- `curl` for downloading embedding models

### Python Dependencies

- `sqlite-utils`
- `pandas`
- `numpy`
- `sqlparse`
- `black`

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/hypergraph-db-api.git
   cd hypergraph-db-api
   ```

2. Install dependencies using Poetry:

   ```bash
   poetry install
   ```

   If you don’t have Poetry installed, follow the instructions [here](https://python-poetry.org/docs/#installation).

3. Download and set up the embedding model:

   ```bash
   just download-model
   ```

   This downloads the `all-MiniLM-L6-v2` model to `sql/models/`.

## Usage

### Initializing the Database

```python
from hypergraph_db import HypergraphDB

# Initialize the database (or connect to an existing one)
db = HypergraphDB("mydatabase.db")
```

This initializes the database schema if needed and loads the `sqlite-vec` and `sqlite-lembed` extensions.

### Inserting Nodes and Hyperedges

A node represents an entity in the hypergraph, and a hyperedge connects multiple nodes.

```python
from hypergraph_db import Node, Hyperedge

# Create a new node
node = Node(body='{"id": "node1", "name": "Alpha"}')
db.insert_node(node)

# Create a hyperedge that connects node1 and node2
hyperedge = Hyperedge(edge_id="edge1", properties='{"relationship": "friend"}', nodes='["node1", "node2"]')
db.insert_hyperedge(hyperedge)

# Map nodes to the hyperedge with specific order
db.insert_node_hyperedge_map("edge1", "node1", 1)
db.insert_node_hyperedge_map("edge1", "node2", 2)
```

### Inserting Embeddings

Generate text embeddings for nodes using `sqlite-lembed`.

```python
from hypergraph_db import EmbeddingMetadata

# Generate and insert an embedding for a node's content
embedding_metadata = EmbeddingMetadata(
    metadata_id="embed1",
    node_id=node.id,
    model="all-MiniLM-L6-v2",
    start_idx=0,
    end_idx=len(node.body),
)
db.insert_embedding(embedding_metadata, node.body)
```

### Batch Inserting Embeddings

Insert multiple embeddings in a single transaction.

```python
embeddings_metadata = [
    EmbeddingMetadata(metadata_id="embed2", node_id="node2", model="all-MiniLM-L6-v2", start_idx=0, end_idx=100),
    EmbeddingMetadata(metadata_id="embed3", node_id="node3", model="all-MiniLM-L6-v2", start_idx=0, end_idx=150),
]
texts = ["This is the content for node 2", "This is the content for node 3"]

db.insert_embeddings_batch(embeddings_metadata, texts)
```

### Searching Nodes

```python
# Search nodes with a specific property
nodes = db.search_nodes_by_property("name", "Alpha")
for n in nodes:
    print(n.to_dict())
```

### Performing Vector Search

```python
# Perform a vector search based on query text
results = db.search_embeddings(query_text="Alpha", top_k=3)
for result in results:
    print(result)
```

### Hypergraph Traversal

```python
# Traverse the hypergraph from node1
traversal = db.traverse_hypergraph("node1")
for node in traversal:
    print(node)
```

### Closing the Database Connection

```python
db.close()
```

## Running Tests

Unit tests are included and can be run with `pytest`.

```bash
poetry add pytest --dev
pytest
```

The test suite includes tests for:

- Inserting and retrieving nodes
- Inserting and updating hyperedges
- Generating and storing embeddings
- Traversing the hypergraph
- Batch operations

## Contributing

Contributions are welcome!

1. Fork the repository.
2. Create a new branch: `git checkout -b feature-branch`.
3. Commit your changes: `git commit -m 'Add new feature'`.
4. Push to the branch: `git push origin feature-branch`.
5. Open a pull request.

Please ensure that your code follows Python best practices and is formatted using Black.

```bash
black .
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Summary

This project provides a Python API for managing a temporal directed hypergraph with text embeddings. It leverages SQLite, `sqlite-vec`, and `sqlite-lembed` to enable efficient storage, retrieval, and querying of nodes, hyperedges, and embeddings.

The API supports:

- Inserting nodes and hyperedges
- Generating and storing text embeddings
- Performing vector similarity searches
- Traversing the hypergraph
- Batch operations for improved performance

Feel free to contribute, report issues, or use the API in your own projects!

