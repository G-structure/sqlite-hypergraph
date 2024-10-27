SELECT e.embedding, m.start_idx, m.end_idx, m.child, m.model
FROM embeddings e
JOIN embedding_metadata m ON e.rowid = m.embedding_id
WHERE m.node_id = ?;