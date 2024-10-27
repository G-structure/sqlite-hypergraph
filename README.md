Hypergraph DB API

A Python API for managing a temporal directed hypergraph SQLite database with text embeddings. This API uses sqlite-vec for vector search and sqlite-lembed for generating text embeddings. It is designed for handling complex graph data, including nodes, hyperedges, and embeddings, while enabling vector similarity searches and batch operations for efficiency.

Key Features

  •	Nodes: Represent entities or objects in the hypergraph. Stored as JSON objects.
  •	Hyperedges: Connect multiple nodes with direction and store additional properties.
  •	Embeddings: Store vector embeddings of node content for semantic searches.
  •	Batch Operations: Insert multiple embeddings or nodes in a single transaction.
  •	Text Embedding Generation: Uses sqlite-lembed to generate embeddings from text.
  •	Vector Search: Leverages sqlite-vec for efficient nearest-neighbor searches.
  •	Hypergraph Traversal: Traverse the hypergraph from any starting node, exploring connected edges and nodes.

Table of Contents

  1.	Requirements
  2.	Installation
  3.	Usage
  •	Initializing the Database
  •	Inserting Nodes and Hyperedges
  •	Inserting Embeddings
  •	Batch Inserting Embeddings
  •	Searching Nodes
  •	Performing Vector Search
  •	Hypergraph Traversal
  4.	Running Tests
  5.	Contributing
  6.	License

Requirements

  •	Python 3.10+
  •	SQLite 3.31.0+ (for JSON and virtual table support)
  •	sqlite-vec and sqlite-lembed SQLite extensions
  •	curl for downloading embedding models

Python Dependencies:

  •	sqlite-utils
  •	pandas
  •	numpy
  •	sqlparse
  •	black

Installation

  1.	Clone the repository:

git clone https://github.com/yourusername/hypergraph-db-api.git
cd hypergraph-db-api


  2.	Install dependencies:
This project uses Poetry for dependency management. If you don’t have Poetry installed, follow the instructions here.
To install the dependencies, run:

poetry install


  3.	Download and set up the embedding model:
We use the all-MiniLM-L6-v2 model from Hugging Face, which has been converted to GGUF format for use with sqlite-lembed.
Use the following command to download the model:

just download-model

This will download the model into the sql/models/ folder.

Usage

Initializing the Database

To start using the hypergraph database, first create an instance of the HypergraphDB class and specify the path to the SQLite database file:

from hypergraph_db import HypergraphDB

# Initialize the database (or connect to an existing one)
db = HypergraphDB("mydatabase.db")

This will automatically initialize the database schema if it hasn’t been created yet, and load the necessary SQLite extensions (sqlite-vec and sqlite-lembed).

Inserting Nodes and Hyperedges

A node represents an entity in the hypergraph, stored as JSON data, and a hyperedge connects multiple nodes.

Insert a Node:

from hypergraph_db import Node

# Create a new node
node = Node(body='{"id": "node1", "name": "Alpha"}')
db.insert_node(node)

Insert a Hyperedge:

from hypergraph_db import Hyperedge

# Create a hyperedge that connects node1 and node2
hyperedge = Hyperedge(edge_id="edge1", properties='{"relationship": "friend"}', nodes='["node1", "node2"]')
db.insert_hyperedge(hyperedge)

# Map the nodes to the hyperedge with specific order
db.insert_node_hyperedge_map("edge1", "node1", 1)
db.insert_node_hyperedge_map("edge1", "node2", 2)

Inserting Embeddings

You can use the sqlite-lembed extension to generate text embeddings for nodes and store them in the hypergraph.

Insert an Embedding:

from hypergraph_db import EmbeddingMetadata

# Generate and insert embedding for a node's content
embedding_metadata = EmbeddingMetadata(
    metadata_id="embed1",
    node_id=node.id,
    model="all-MiniLM-L6-v2",
    start_idx=0,
    end_idx=len(node.body),
)
db.insert_embedding(embedding_metadata, node.body)

Batch Inserting Embeddings

To improve performance when dealing with large datasets, you can batch insert embeddings.

# List of embeddings metadata and corresponding texts
embeddings_metadata = [
    EmbeddingMetadata(metadata_id="embed2", node_id="node2", model="all-MiniLM-L6-v2", start_idx=0, end_idx=100),
    EmbeddingMetadata(metadata_id="embed3", node_id="node3", model="all-MiniLM-L6-v2", start_idx=0, end_idx=150),
]
texts = ["This is the content for node 2", "This is the content for node 3"]

# Batch insert embeddings
db.insert_embeddings_batch(embeddings_metadata, texts)

Searching Nodes

You can search for nodes by properties stored in their JSON data.

# Search nodes with a specific property
nodes = db.search_nodes_by_property("name", "Alpha")
for n in nodes:
    print(n.to_dict())

Performing Vector Search

After embeddings have been generated and stored, you can perform vector similarity searches using sqlite-vec.

# Perform a vector search based on query text
results = db.search_embeddings(query_text="Alpha", top_k=3)
for result in results:
    print(result)

Hypergraph Traversal

You can traverse the hypergraph, starting from a particular node, and explore connected nodes and hyperedges.

# Traverse the hypergraph from node1
traversal = db.traverse_hypergraph("node1")
for node in traversal:
    print(node)

Closing the Database Connection

Always close the database connection when you’re done using it:

db.close()

Running Tests

Unit tests for the hypergraph database are included and can be run using pytest. Make sure you have pytest installed:

poetry add pytest --dev

To run the tests:

pytest

The test suite includes tests for:

  •	Inserting and retrieving nodes
  •	Inserting and updating hyperedges
  •	Generating and storing embeddings
  •	Traversing the hypergraph
  •	Batch operations

Contributing

Contributions are welcome! If you’d like to contribute, please follow these steps:

  1.	Fork the repository.
  2.	Create a new branch (git checkout -b feature-branch).
  3.	Commit your changes (git commit -m 'Add new feature').
  4.	Push to the branch (git push origin feature-branch).
  5.	Open a pull request.

Please ensure that your code follows Python best practices and is formatted using Black.

To format the code with Black:

black .

License

This project is licensed under the MIT License. See the LICENSE file for details.

Summary

This project provides a fully functional Python API for managing a temporal directed hypergraph with text embeddings. It leverages SQLite, sqlite-vec, and sqlite-lembed to enable efficient storage, retrieval, and querying of nodes, hyperedges, and embeddings.

The API supports:

  •	Inserting nodes and hyperedges
  •	Generating and storing text embeddings
  •	Performing vector similarity searches
  •	Traversing the hypergraph
  •	Batch operations for improved performance

Feel free to contribute, report issues, or use the API in your own projects!