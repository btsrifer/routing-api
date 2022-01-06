CREATE TABLE IF NOT EXISTS nodes
  (
     node_id VARCHAR(3) NOT NULL PRIMARY KEY,
     name VARCHAR(64) NOT NULL
  );
CREATE TABLE IF NOT EXISTS edges
  (
     edge_id INTEGER NOT NULL PRIMARY KEY,
     origin_id VARCHAR(3) NOT NULL,
     destination_id VARCHAR(3) NOT NULL,
     cost FLOAT NOT NULL,
     FOREIGN KEY(origin_id) REFERENCES nodes(node_id),
     FOREIGN KEY(destination_id) REFERENCES nodes(node_id)
  ); 