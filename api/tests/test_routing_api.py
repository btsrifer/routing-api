from django.test import Client, TestCase


class TestRoutingAPI(TestCase):
    """Test cases for the routing app."""

    def setUp(self) -> None:
        client = Client()

    def test_routing_endpoint(self) -> None:
        """Valid request on /routing endpoint."""

        request_payload = {
            "origin": "A",
            "destination": "B",
            "cutoff": 1,
        }
        r = self.client.post("/routing", request_payload)

        # Assert response status code.
        self.assertEqual(r.status_code, 200)

        # Assert response payload.
        expected_response = {
            "paths_collection_summary": {
                "number_of_paths": 1,
                "shorter_path": 1,
                "longest_path": 1,
                "cheapest_path": 1.2,
                "most_expensive_path": 1.2,
            },
            "paths": [
                {
                    "path_summary": {
                        "route": "AB",
                        "number_of_connections": 1,
                        "total_cost": 1.2,
                    },
                    "connections": [
                        {"edge_id": 1, "origin": "A", "destination": "B", "cost": 1.2}
                    ],
                }
            ],
        }
        self.assertDictEqual(r.json(), expected_response)
