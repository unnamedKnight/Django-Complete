from django.db import models
import uuid

# Create your models here.


class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    featured_image = models.ImageField(
        default="default.jpg",
        upload_to="images/user_uploaded_content",
        blank=True,
        null=True,
    )
    demo_link = models.CharField(max_length=2000, null=True, blank=True)
    tags = models.ManyToManyField("Tag", blank=True)
    vote_total = models.IntegerField(null=True, blank=True, default=0)
    vote_ratio = models.IntegerField(null=True, blank=True, default=0)
    source_code = models.CharField(max_length=2000, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, unique=True, editable=False
    )

    def __str__(self) -> str:
        return f'{self.title}-->{self.id}'


# text choices value field in Review Model
class VoteTypes(models.TextChoices):
    UP_VOTE = ("up", "Up vote")
    DOWN_VOTE = ("down", "Down vote")


class Review(models.Model):
    # review_owner = models.ForeignKey()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=50, choices=VoteTypes.choices)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, unique=True, editable=False
    )

    def __str__(self) -> str:
        return self.value


class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, unique=True, editable=False
    )

    def __str__(self) -> str:
        return self.name
