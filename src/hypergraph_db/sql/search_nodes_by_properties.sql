SELECT id, body
FROM nodes
WHERE json_extract(body, ?) = ?;

