-- Nodes Table with Timestamps
CREATE TABLE IF NOT EXISTS nodes (
    body TEXT,
    id TEXT GENERATED ALWAYS AS (json_extract(body, '$.id')) VIRTUAL NOT NULL UNIQUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS id_idx ON nodes(id);

-- Hyperedges Table with Timestamps and Direction Information
CREATE TABLE IF NOT EXISTS hyperedges (
    id TEXT PRIMARY KEY,
    properties TEXT,
    nodes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS hyperedge_idx ON hyperedges(id);

-- Node-Hyperedge Mapping with Order and Timestamps
CREATE TABLE IF NOT EXISTS node_hyperedge_map (
    hyperedge_id TEXT,
    node_id TEXT,
    node_order INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(hyperedge_id) REFERENCES hyperedges(id),
    FOREIGN KEY(node_id) REFERENCES nodes(id)
);

CREATE INDEX IF NOT EXISTS node_hyperedge_map_idx ON node_hyperedge_map(hyperedge_id, node_id, node_order);

-- Embeddings Table using vec0 virtual table
CREATE VIRTUAL TABLE IF NOT EXISTS embeddings USING vec0(
    embedding float[384]
);

-- Embedding Metadata Table
CREATE TABLE IF NOT EXISTS embedding_metadata (
    id TEXT PRIMARY KEY,
    node_id TEXT,
    embedding_id INTEGER,
    model TEXT,
    start_idx INTEGER,
    end_idx INTEGER,
    child TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(node_id) REFERENCES nodes(id),
    FOREIGN KEY(embedding_id) REFERENCES embeddings(rowid)
);

CREATE INDEX IF NOT EXISTS embedding_node_idx ON embedding_metadata(node_id);