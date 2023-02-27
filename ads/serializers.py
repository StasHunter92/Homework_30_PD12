from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from ads.models import Category, Advertisement


# ----------------------------------------------------------------------------------------------------------------------
# Category serializers
class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for ViewSet
    """
    class Meta:
        model: Category = Category
        fields: str = "__all__"


# ----------------------------------------------------------------------------------------------------------------------
# Advertisement serializers
class AdvertisementListSerializer(serializers.ModelSerializer):
    """
    Serializer for ListView
    """
    author: serializers.SlugRelatedField = serializers.SlugRelatedField(read_only=True, slug_field="first_name")
    category: serializers.SlugRelatedField = serializers.SlugRelatedField(read_only=True, slug_field="name")

    class Meta:
        model: Advertisement = Advertisement
        exclude: list[str] = ["is_published"]


class AdvertisementDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for DetailView
    """
    author: serializers.SlugRelatedField = serializers.SlugRelatedField(read_only=True, slug_field="first_name")
    category: serializers.SlugRelatedField = serializers.SlugRelatedField(read_only=True, slug_field="name")
    locations: SerializerMethodField = SerializerMethodField()

    def get_locations(self, advertisement) -> list:
        """
        Get list of locations

        :param advertisement: Object of advertisement
        :return: List of locations
        """
        return [location.name for location in advertisement.author.locations.all()]

    class Meta:
        model: Advertisement = Advertisement
        fields: list[str] = ['name', 'author', 'price', 'description', 'is_published', 'image', 'category', 'locations']


class AdvertisementCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for CreateView
    """
    image: serializers.ImageField = serializers.ImageField(required=False)

    class Meta:
        model: Advertisement = Advertisement
        fields: str = "__all__"

    def is_valid(self, raise_exception=False) -> bool:
        """
        Validate data

        :return: True of False
        """
        self.initial_data['author'] = self.context['request'].user.id

        return super().is_valid(raise_exception=raise_exception)

    def create(self, data):
        """
        Create a new advertisement
        """
        advertisement = super().create(data)

        return advertisement


class AdvertisementUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for UpdateView
    """
    class Meta:
        model: Advertisement = Advertisement
        fields: str = "__all__"

    def is_valid(self, raise_exception=False) -> bool:
        """
        Validate data

        :return: True of False
        """
        self.initial_data['author'] = self.context['request'].user.id

        return super().is_valid(raise_exception=raise_exception)

    def save(self):
        """
        Save changes to advertisement
        """
        advertisement = super().save()

        return advertisement


class AdvertisementDeleteSerializer(serializers.ModelSerializer):
    """
    Serializer for DeleteView
    """
    class Meta:
        model: Advertisement = Advertisement
        fields: list[str] = ["id"]
