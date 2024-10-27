SELECT nodes.id, nodes.body
FROM nodes
JOIN node_hyperedge_map ON nodes.id = node_hyperedge_map.node_id
WHERE node_hyperedge_map.hyperedge_id = ?;