from rest_framework import serializers
from routing.models import RoutingOptionsModel


class RoutingOptionsSerializer(serializers.ModelSerializer):
    """Serializer for the /routing endpoint."""

    def create(self, validated_data: dict) -> RoutingOptionsModel:
        """Returns an instance of a RoutingOptionsModel after successfully
        serializing the request payload."""
        return RoutingOptionsModel(**validated_data)

    class Meta:
        model = RoutingOptionsModel
        fields = "__all__"
