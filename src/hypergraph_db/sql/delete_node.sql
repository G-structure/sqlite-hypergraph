DELETE FROM nodes WHERE id = '{node_id}';
DELETE FROM node_hyperedge_map WHERE node_id = '{node_id}';
DELETE FROM embedding_metadata WHERE node_id = '{node_id}';