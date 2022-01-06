# About
This project provides a sample API that generates paths between an origin and destination in a network. The API is designed in python using the `Django REST Framework` and the network functionalities are implemented using the `NetworkX` library. The design of this project assumes that the data that define the network topology (i.e. nodes and edges) reside on an external database. When the container of the project is executed for the first time, a sample external database is created and populated with a sample network.

# Build

1. `Docker Desktop` should be installed and running (or `Docker` and `Docker Compose`).
2. Change directory to the project's root directory: `cd .../routing-api`
3. Execute: `docker compose up`
4. You can access the API on `http://localhost:8000/routing` with the `POST` method. Use the postman collection present in the `docs` folder to experiment with the API. For information about the request payload format, look at the `Request payload format` section.
    - Alternatively you can try a sample request from your terminal, i.e. like: 
    ```
        curl --location --request POST 'http://localhost:8000/routing' \
        --header 'Content-Type: application/json' \
        --data-raw '{
            "origin": "A",
            "destination": "B"
        }'
    ```

# Network data
The external database is the `routing` database and it resides on the PostgreSQL image container alongside the Django REST database (called `api`). To have a look on the sample network topology data of the external database:

1. Change directory to the project's root directory and run the PostgreSQL image container: `docker compose run api_db`
2. On a separate terminal window, change again directory to the project's root directory and execute:
    - `docker compose exec api_db psql -U postgres -d routing -c "select * from nodes;"`
    - `docker compose exec api_db psql -U postgres -d routing -c "select * from edges;"`

The `nodes` table data look like:
```
 node_id |  name  
---------+--------
 A       | Node_A
 B       | Node_B
 C       | Node_C
...
```
And the `edges` table data look like:
```
 edge_id | origin_id | destination_id | cost 
---------+-----------+----------------+------
       1 | A         | B              |  1.2
       2 | A         | C              |  3.2
       3 | A         | D              |  0.8
       4 | B         | G              |  0.5
       5 | B         | A              |  1.5
...
```
__\*__ The `cost` quantity is associated with every edge and it describes in an abstract manner how "costly" is the transition in a pair of connected nodes. It is just introduced to bring an extra dimension to the path generation process.       
# Request payload format
The format of the request payload is the following:
```json
{
    "origin": "A",
    "destination": "I",
    "cutoff": 5,    
    "plus_on_min_length": 1,
    "plus_on_min_cost": 5
}
```
| Attribute | Description | Type | Required |
| :---      |   :----:    | :--: |    ---:  |
| origin | Node in the network in which the path begins. | string | YES |
| destination | Node in the network in which the path ends up. | string | YES |
| cutoff | Maximum number of edges (connections) allowed in the path (path length). | integer | NO |
| plus_on_min_length | Number that specifies that the maximum number of connections allowed in the path will be equal to the number  of connections present in the shortest path plus this number. E.g. if `plus_on_min_length` is equal to 2 and the shorted path between the origin and the destination has 3 edges, then the maximum number of connections allowed in the computed paths will be 5. | integer | NO |
| plus_on_min_cost | Each edge between 2 nodes has an associated cost. This attribute specifies that the maximum cost of the computed paths on the network will be equal to the cost of the cheapest path plus this value (`plus_on_min_cost`). | float | NO |


__\*__ It does not make a lot of sense to define both the `cutoff` and `plus_on_min_length` attributes on the same request (although the API can handle it). The above payload format is just a sample to demonstrate the attributes.

# Response payload format
The format of the response payload is the following:
```json
{
    "paths_collection_summary": {
        "number_of_paths": 2,
        "shorter_path": 3,
        "longest_path": 4,
        "cheapest_path": 3.2,
        "most_expensive_path": 7.9
    },
    "paths": [
        {
            "path_summary": {
                "route": "ABGFI",
                "number_of_connections": 4,
                "total_cost": 7.9
            },
            "connections": [
                {
                    "edge_id": 1,
                    "origin": "A",
                    "destination": "B",
                    "cost": 1.2
                },
                {
                    "edge_id": 4,
                    "origin": "B",
                    "destination": "G",
                    "cost": 0.5
                },
                {
                    "edge_id": 17,
                    "origin": "G",
                    "destination": "F",
                    "cost": 2.2
                },
                {
                    "edge_id": 15,
                    "origin": "F",
                    "destination": "I",
                    "cost": 4.0
                }
            ]
        },
        {
            "path_summary": {
                "route": "ABGI",
                "number_of_connections": 3,
                "total_cost": 3.2
            },
            "connections": [
                {
                    "edge_id": 1,
                    "origin": "A",
                    "destination": "B",
                    "cost": 1.2
                },
                {
                    "edge_id": 4,
                    "origin": "B",
                    "destination": "G",
                    "cost": 0.5
                },
                {
                    "edge_id": 18,
                    "origin": "G",
                    "destination": "I",
                    "cost": 1.5
                }
            ]
        }
    ]
}
```