from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django_resized import ResizedImageField


class User(AbstractUser):
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True, blank=True)
    hackathon_participant = models.BooleanField(default=True, null=True)
    avatar = ResizedImageField(size=[300, 300], default="avatar.png")
    # 	twitter = models.URLField(max_length=500)
    # 	linkedin = models.URLField(max_length=500)
    # 	website = models.URLField(max_length=500)
    # 	facebook = models.URLField(max_length=500)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]


class Event(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    participation = models.ManyToManyField(User, blank=True, related_name="events")
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField()
    registration_deadline = models.DateTimeField(null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Submission(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )
    participant = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="submissions"
    )
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True)
    details = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.participant) + "---" + str(self.event)
