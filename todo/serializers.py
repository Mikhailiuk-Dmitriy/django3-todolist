from rest_framework import serializers  # type: ignore

from .models import Todo


class TodoSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Todo
        fields = "__all__"
