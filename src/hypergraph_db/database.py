import sqlite3
from typing import List, Optional, Any, Dict
from pathlib import Path

from .models import Node, Hyperedge, EmbeddingMetadata
from .sql import SQLScripts
from .utils import load_extensions, dict_factory


class HypergraphDB:
    def __init__(self, db_path: str):
        """Initialize the connection and set up the database."""
        self.connection = sqlite3.connect(db_path)
        self.connection.row_factory = dict_factory
        load_extensions(self.connection)  # Load SQLite extensions
        self._initialize_schema()  # Initialize the schema

    def _initialize_schema(self):
        """Initializes the database schema by executing the schema SQL."""
        schema_sql = SQLScripts.get_script("schema.sql")
        with self.connection:
            self.connection.executescript(schema_sql)

    def execute_sql(self, sql: str, params: Optional[List[Any]] = None):
        """Execute raw SQL commands."""
        with self.connection:
            cursor = self.connection.execute(sql, params or [])
        return cursor

    # Node-related operations
    def insert_node(self, node: Node):
        """Insert a new node into the database."""
        sql = SQLScripts.get_script("insert_node.sql")
        with self.connection:
            self.connection.execute(sql, (node.body,))
            # Get the generated node ID from the body JSON
            node_id = self.connection.execute(
                "SELECT id FROM nodes WHERE rowid = last_insert_rowid()"
            ).fetchone()["id"]
        node.id = node_id
        return node

    def update_node(self, node_id: str, new_body: str):
        """Update an existing node."""
        sql = SQLScripts.get_script("update_node.sql")
        with self.connection:
            self.connection.execute(sql, (new_body, node_id))

    def delete_node(self, node_id: str):
        """Delete a node and its related edges and embeddings."""
        sql = SQLScripts.get_script("delete_node.sql")
        with self.connection:
            self.connection.executescript(sql.format(node_id=node_id))

    def get_node_by_id(self, node_id: str) -> Optional[Node]:
        """Retrieve a node by its ID."""
        cursor = self.connection.execute("SELECT * FROM nodes WHERE id = ?", (node_id,))
        row = cursor.fetchone()
        if row:
            return Node(body=row["body"], node_id=row["id"])
        return None

    def search_nodes_by_property(self, key: str, value: Any) -> List[Node]:
        """Search for nodes based on properties in their JSON body."""
        sql = SQLScripts.get_script("search_nodes_by_properties.sql")
        sql = sql.replace("$.key", f"$['{key}']")
        cursor = self.connection.execute(sql, (value,))
        rows = cursor.fetchall()
        return [Node(body=row["body"], node_id=row["id"]) for row in rows]

    # Hyperedge-related operations
    def insert_hyperedge(self, hyperedge: Hyperedge):
        """Insert a new hyperedge into the database."""
        sql = SQLScripts.get_script("insert_hyperedge.sql")
        with self.connection:
            self.connection.execute(
                sql, (hyperedge.id, hyperedge.properties, hyperedge.nodes)
            )

    def update_hyperedge(self, hyperedge_id: str, new_properties: str):
        """Update an existing hyperedge."""
        sql = SQLScripts.get_script("update_hyperedge.sql")
        with self.connection:
            self.connection.execute(sql, (new_properties, hyperedge_id))

    def delete_hyperedge(self, hyperedge_id: str):
        """Delete a hyperedge and its related node mappings."""
        sql = SQLScripts.get_script("delete_hyperedge.sql")
        with self.connection:
            self.connection.executescript(sql.format(hyperedge_id=hyperedge_id))

    def insert_node_hyperedge_map(
        self, hyperedge_id: str, node_id: str, node_order: int
    ):
        """Map a node to a hyperedge with a specific order."""
        sql = SQLScripts.get_script("insert_node_hyperedge_map.sql")
        with self.connection:
            self.connection.execute(sql, (hyperedge_id, node_id, node_order))

    def search_hyperedges(self, node_ids: List[str]):
        """Search for hyperedges that connect specific nodes."""
        sql = SQLScripts.get_script("search_hyperedges.sql")
        placeholders = ",".join(["?"] * len(node_ids))
        query = sql.replace("?", placeholders, 1)
        params = node_ids + [len(node_ids)]
        cursor = self.connection.execute(query, params)
        return cursor.fetchall()

    # Embedding-related operations
    def insert_embedding(self, embedding_metadata: EmbeddingMetadata, text: str):
        """Generate and insert an embedding using sqlite-lembed."""
        # Generate embedding using lembed() function
        embedding_sql = """
        SELECT lembed(?, ?) AS embedding
        """
        cursor = self.connection.execute(embedding_sql, ("all-MiniLM-L6-v2", text))
        embedding_row = cursor.fetchone()
        embedding = embedding_row["embedding"]

        # Insert embedding into embeddings table
        insert_embedding_sql = SQLScripts.get_script("insert_embedding.sql")
        with self.connection:
            self.connection.execute(insert_embedding_sql, (embedding,))
            embedding_id = self.connection.execute(
                "SELECT last_insert_rowid() as id"
            ).fetchone()["id"]
            embedding_metadata.embedding_id = embedding_id

            # Insert embedding metadata
            self.connection.execute(
                """
                INSERT INTO embedding_metadata 
                (id, node_id, embedding_id, model, start_idx, end_idx, child) 
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    embedding_metadata.id,
                    embedding_metadata.node_id,
                    embedding_metadata.embedding_id,
                    embedding_metadata.model,
                    embedding_metadata.start_idx,
                    embedding_metadata.end_idx,
                    embedding_metadata.child,
                ),
            )

    def insert_embeddings_batch(
        self, embeddings_metadata: List[EmbeddingMetadata], texts: List[str]
    ):
        """Generate and insert embeddings in batch."""
        embeddings = []
        for text in texts:
            cursor = self.connection.execute(
                "SELECT lembed(?, ?) AS embedding", ("all-MiniLM-L6-v2", text)
            )
            embedding_row = cursor.fetchone()
            embeddings.append((embedding_row["embedding"],))

        # Insert embeddings in batch
        insert_embedding_sql = "INSERT INTO embeddings (embedding) VALUES (?)"
        with self.connection:
            self.connection.executemany(insert_embedding_sql, embeddings)
            # Get the last rowid after batch insert
            last_rowid = self.connection.execute(
                "SELECT last_insert_rowid()"
            ).fetchone()[0]
            first_rowid = last_rowid - len(embeddings) + 1
            embedding_ids = list(range(first_rowid, last_rowid + 1))

            # Insert embedding metadata in batch
            metadata_tuples = []
            for meta, eid in zip(embeddings_metadata, embedding_ids):
                meta.embedding_id = eid
                metadata_tuples.append(
                    (
                        meta.id,
                        meta.node_id,
                        meta.embedding_id,
                        meta.model,
                        meta.start_idx,
                        meta.end_idx,
                        meta.child,
                    )
                )
            self.connection.executemany(
                """
                INSERT INTO embedding_metadata 
                (id, node_id, embedding_id, model, start_idx, end_idx, child) 
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                metadata_tuples,
            )

    def search_embeddings(self, query_text: str, top_k: int = 5):
        """Perform vector search using sqlite-vec."""
        # Generate embedding for the query text
        cursor = self.connection.execute(
            "SELECT lembed(?, ?) AS embedding", ("all-MiniLM-L6-v2", query_text)
        )
        query_embedding_row = cursor.fetchone()
        query_embedding = query_embedding_row["embedding"]

        # Perform KNN search using vec0 virtual table
        search_sql = """
        SELECT
            m.node_id,
            m.start_idx,
            m.end_idx,
            m.model,
            m.child,
            e.rowid,
            e.distance
        FROM embeddings e
        JOIN embedding_metadata m ON e.rowid = m.embedding_id
        WHERE e.embedding MATCH ?
        ORDER BY e.distance
        LIMIT ?
        """
        cursor = self.connection.execute(search_sql, (query_embedding, top_k))
        return cursor.fetchall()

    # Hypergraph traversal
    def traverse_hypergraph(self, start_node: str) -> List[Dict[str, Any]]:
        """Traverse the hypergraph starting from a given node."""
        sql = SQLScripts.get_script("traverse_hypergraph.sql")
        cursor = self.connection.execute(sql, (start_node,))
        return cursor.fetchall()

    def close(self):
        """Close the database connection."""
        self.connection.close()
