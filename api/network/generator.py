from functools import cached_property

from network.graph_constructor import RoutingGraph
from network.models import Path, PathsCollection
from routing.models import RoutingOptionsModel


class PathsGenerator:
    """This class provides methods to generate PathsCollection on RoutingGraph
    based on the specified RoutingOptionsModel."""

    def __init__(self, routing_options: RoutingOptionsModel) -> None:
        self.oringin: str = routing_options.origin
        self.destination: str = routing_options.destination
        self.cutoff: int = routing_options.cutoff
        self.plus_on_min_length: int = routing_options.plus_on_min_length
        self.plus_on_min_cost: float = routing_options.plus_on_min_cost

    @cached_property
    def _raw_paths(self) -> list[Path]:
        """All the paths (with no repeated nodes) in RoutingGraph from
        self.origin to self.destination. If self.cutoff is not None, the maximum
        length path allows is the value of self.cutoff"""

        return RoutingGraph().paths_between(
            origin=self.oringin,
            destination=self.destination,
            cutoff=self.cutoff if self.cutoff is not None else None,
        )

    @cached_property
    def min_path_length(self) -> float:
        """Min path length in self._raw_paths ."""

        return min(len(path.connections) for path in self._raw_paths)

    @cached_property
    def min_cost(self) -> float:
        """Min path cost in self._raw_path ."""

        return min(
            sum(connection.cost for connection in path.connections)
            for path in self._raw_paths
        )

    def _filter_based_on_connections(self, path: Path) -> bool:
        _len = len(path.connections)
        if _len == 1 or self.plus_on_min_length is None:
            return True

        return _len <= self.min_path_length + self.plus_on_min_length

    def _filter_based_on_cost(self, path: Path) -> None:
        if self.plus_on_min_cost is None:
            return True

        return (
            sum(connection.cost for connection in path.connections)
            <= self.min_cost + self.plus_on_min_cost
        )

    @cached_property
    def valid_paths(self) -> PathsCollection:
        """Valid paths in RoutingGraph from self.origin to self.destination.
        Valid paths are considered the paths that go through the filtering applied
        of this function."""

        filters = (
            lambda path: self._filter_based_on_connections(path),
            lambda path: self._filter_based_on_cost(path),
        )
        filtered_paths = filter(
            lambda path: all(applied_filter(path) for applied_filter in filters),
            self._raw_paths,
        )
        return PathsCollection.from_list(list(filtered_paths))
