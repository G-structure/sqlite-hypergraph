DELETE FROM hyperedges WHERE id = '{hyperedge_id}';
DELETE FROM node_hyperedge_map WHERE hyperedge_id = '{hyperedge_id}';