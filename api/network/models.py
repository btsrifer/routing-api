from pydantic import BaseModel


class Node(BaseModel):
    """Class representing a graph node."""

    node_id: str
    name: str

    @classmethod
    def from_db_record(cls, record: tuple):
        """Factory from a tuple corresponding to a database record."""
        return cls.parse_obj(zip(cls.__dict__["__fields__"].keys(), record))


class Edge(BaseModel):
    """Class representing a graph edge."""

    edge_id: int
    origin: str
    destination: str
    cost: float

    @classmethod
    def from_db_record(cls, record: tuple):
        """Factory from a tuple corresponding to a database record."""
        return cls.parse_obj(zip(cls.__dict__["__fields__"].keys(), record))


class Path(BaseModel):
    """Class representing a path consisting of many connections between nodes."""

    class Summary(BaseModel):
        """Summary information for a Path."""

        route: str
        number_of_connections: int
        total_cost: float

        @classmethod
        def from_list(cls, _list: list[Edge]):
            return cls.parse_obj(
                {
                    "route": f"{_list[0].origin}{_list[0].destination}"
                    if len(_list) == 1
                    else "".join([connetion.origin for connetion in _list[:-1]])
                    + f"{_list[-1].origin}{_list[-1].destination}",
                    "number_of_connections": len(_list),
                    "total_cost": round(
                        sum(connection.cost for connection in _list), 2
                    ),
                }
            )

    path_summary: Summary
    connections: list[Edge]

    @classmethod
    def from_list(cls, _list: list[Edge]):
        return cls.parse_obj(
            {"connections": _list, "path_summary": cls.Summary.from_list(_list)}
        )


class PathsCollection(BaseModel):
    """Class representing the valid paths between two nodes
    (an origin and a destination)."""

    class Summary(BaseModel):
        """Summary information for a PathsCollection."""

        number_of_paths: int
        shorter_path: int
        longest_path: int
        cheapest_path: float
        most_expensive_path: float

        @classmethod
        def from_list(cls, _list: list[Path]):
            return cls.parse_obj(
                {
                    "number_of_paths": len(_list),
                    "shorter_path": min(len(path.connections) for path in _list),
                    "longest_path": max(len(path.connections) for path in _list),
                    "cheapest_path": round(
                        min(
                            sum(connection.cost for connection in path.connections)
                            for path in _list
                        ),
                        2,
                    ),
                    "most_expensive_path": round(
                        max(
                            sum(connection.cost for connection in path.connections)
                            for path in _list
                        ),
                        2,
                    ),
                }
            )

    paths_collection_summary: Summary
    paths: list[Path]

    @classmethod
    def from_list(cls, _list):
        """Factory from a list of paths."""
        return cls.parse_obj(
            {"paths": _list, "paths_collection_summary": cls.Summary.from_list(_list)}
        )
