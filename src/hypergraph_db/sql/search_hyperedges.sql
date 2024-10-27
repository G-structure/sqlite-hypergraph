SELECT hyperedge_id
FROM node_hyperedge_map
WHERE node_id IN (?, ?)
GROUP BY hyperedge_id
HAVING COUNT(DISTINCT node_id) = ?;