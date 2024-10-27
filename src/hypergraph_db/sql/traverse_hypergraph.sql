WITH RECURSIVE traverse(node_id, depth, created_at) AS (
  SELECT node_id, 0, created_at
  FROM node_hyperedge_map
  WHERE node_id = ?
  UNION
  SELECT nh.node_id, t.depth + 1, nh.created_at
  FROM node_hyperedge_map nh
  JOIN traverse t ON t.node_id = nh.node_id
  WHERE nh.node_order > t.depth
)
SELECT * FROM traverse;