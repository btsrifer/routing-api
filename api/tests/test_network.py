import unittest

from network.graph_constructor import RoutingGraph


class NetworkTestCase(unittest.TestCase):
    """Test cases for the Network module."""

    def test_routing_graph(self) -> None:
        """Test RoutingGraph generation."""

        g = RoutingGraph().graph

        # Assert nodes.
        self.assertCountEqual(g.nodes(), ["A", "B", "C", "D", "E", "F", "G", "H", "I"])

        # Assert edges.
        self.assertCountEqual(
            g.edges(),
            [
                ("A", "B"),
                ("A", "C"),
                ("A", "D"),
                ("B", "G"),
                ("B", "A"),
                ("B", "E"),
                ("C", "E"),
                ("D", "H"),
                ("D", "A"),
                ("E", "B"),
                ("E", "H"),
                ("E", "C"),
                ("E", "F"),
                ("F", "E"),
                ("F", "I"),
                ("F", "H"),
                ("G", "F"),
                ("G", "I"),
                ("H", "F"),
                ("H", "D"),
                ("H", "E"),
                ("I", "F"),
                ("I", "G"),
            ],
        )
