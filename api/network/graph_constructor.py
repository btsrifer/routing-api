from functools import cached_property

import networkx as nx
from network.data_loader import Loader
from network.models import Edge, Node, Path
from networkx.algorithms.simple_paths import all_simple_edge_paths


class RoutingGraph:
    """Graph used to generate the network paths."""

    def __init__(self) -> None:
        db_loader = Loader()
        self.nodes: list[Node] = db_loader.fetch_nodes()
        self.edges: list[Edge] = db_loader.fetch_edges()
        self.G = nx.MultiDiGraph()

    @cached_property
    def graph(self) -> nx.MultiDiGraph:
        """Multi-directional graph with nodes self.nodes and edges self.edges."""

        self._add_nodes()
        self._add_edges()
        return self.G

    def _add_nodes(self) -> None:
        """Add multiple nodes in self.G from self.nodes ."""
        self.G.add_nodes_from(
            [
                (
                    node.node_id,  # Node
                    {**node.__dict__},  # Node attached data
                )
                for node in self.nodes
            ]
        )

    def _add_edges(self) -> None:
        """Add multiple edges in self.G from self.edges ."""
        self.G.add_edges_from(
            [
                (
                    edge.origin,  # Edge from node
                    edge.destination,  # Edge to node
                    {**edge.__dict__},  # Edge attached data
                )
                for edge in self.edges
            ]
        )

    def paths_between(
        self, origin: str, destination: str, cutoff: int = None
    ) -> list[Path]:
        """Calculates all the paths between origin and destination with no
        repeated nodes."""
        return [
            Path.from_list(
                [
                    Edge(
                        **self.graph.get_edge_data(
                            edge_origin, edge_destination, edge_key
                        )
                    )
                    for edge_origin, edge_destination, edge_key in path
                ]
            )
            for path in all_simple_edge_paths(
                self.graph, origin, destination, cutoff=cutoff
            )
        ]
