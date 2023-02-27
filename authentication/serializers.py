from rest_framework import serializers

from authentication.models import User
from locations.models import Location


# ----------------------------------------------------------------------------------------------------------------------
# User serializers
class UserListSerializer(serializers.ModelSerializer):
    """
    Serializer for ListView
    """
    locations: serializers.SlugRelatedField = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name"
    )

    class Meta:
        model: User = User
        exclude: list[str] = ["password", "is_superuser", "is_staff", "is_active", "role", "groups", "user_permissions"]


class UserDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for DetailView
    """
    locations: serializers.SlugRelatedField = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name"
    )

    class Meta:
        model: User = User
        exclude: list[str] = ["id"]


class UserCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for CreateView
    """
    role: serializers.CharField = serializers.CharField(read_only=True)
    locations: serializers.SlugRelatedField = serializers.SlugRelatedField(
        required=False,
        many=True,
        queryset=Location.objects.all(),
        slug_field="name"
    )

    class Meta:
        model: User = User
        fields: str = "__all__"

    def is_valid(self, raise_exception=False) -> bool:
        """
        Validate data

        :return: True of False
        """
        self._locations: list = self.initial_data.pop('locations', [])
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        """
        Create a new user
        """
        user = super().create(validated_data)

        user.set_password(user.password)

        if len(self._locations) > 0:
            for location in self._locations:
                location_obj, _ = Location.objects.get_or_create(name=location)
                user.locations.add(location_obj)
        user.save()

        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for UpdateView
    """
    id: serializers.IntegerField = serializers.IntegerField(read_only=True)
    locations: serializers.SlugRelatedField = serializers.SlugRelatedField(
        required=False,
        many=True,
        queryset=Location.objects.all(),
        slug_field="name"
    )

    class Meta:
        model: User = User
        fields: str = "__all__"

    def is_valid(self, raise_exception=False) -> bool:
        """
        Validate data

        :return: True of False
        """
        self._locations: list = self.initial_data.pop('locations', [])

        return super().is_valid(raise_exception=raise_exception)

    def save(self):
        """
        Save changes to user
        """
        user = super().save()

        if len(self._locations) > 0:
            for location in self._locations:
                location_obj, _ = Location.objects.get_or_create(name=location)
                user.locations.add(location_obj)

        user.save()

        return user


class UserDeleteSerializer(serializers.ModelSerializer):
    """
    Serializer for DeleteView
    """
    class Meta:
        model: User = User
        fields: list[str] = ["id"]
