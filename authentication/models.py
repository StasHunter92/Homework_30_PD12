from django.contrib.auth.models import AbstractUser
from django.db.models import PositiveIntegerField, ManyToManyField, CharField, TextChoices

from locations.models import Location


# ----------------------------------------------------------------------------------------------------------------------
# Create user model
class User(AbstractUser):
    class Roles(TextChoices):
        ADMIN = "admin", "Администратор"
        MODERATOR = "moderator", "Модератор"
        MEMBER = "member", "Пользователь"

    age: PositiveIntegerField = PositiveIntegerField(null=True)
    locations: ManyToManyField = ManyToManyField(Location, default=[])
    role: CharField = CharField(max_length=9, choices=Roles.choices, default=Roles.MEMBER)

    class Meta:
        verbose_name: str = "Пользователь"
        verbose_name_plural: str = "Пользователи"

        ordering: list[str] = ["username"]

    def __str__(self):
        return self.username
