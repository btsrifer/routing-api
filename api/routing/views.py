from network.generator import PathsGenerator
from network.graph_constructor import RoutingGraph
from network.models import PathsCollection
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from routing.serializers import RoutingOptionsSerializer


class RoutingAPIView(APIView):
    """API view for the /routing endpoint."""

    def post(self, request: Request) -> Response:
        """POST method on the /routing endpoint."""

        serializer = RoutingOptionsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        routing_options = serializer.create(validated_data=serializer.validated_data)
        paths: PathsCollection = PathsGenerator(routing_options).valid_paths

        return Response(paths.dict())
