from django.db import models
import uuid
from user_profiles.models import Profile

# Create your models here.


class Project(models.Model):
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    featured_image = models.ImageField(
        default="default.jpg",
        upload_to="images/user_uploaded_content",
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
        return f"{self.title}-->{self.id}"

    @property
    def reviewrs(self) -> list():
        """Returns a list of reviewrs of a given project."""
        return self.review_set.all().values_list("review_owner", flat=True)


    @property
    def get_vote_count(self):
        reviews = self.reviews_set.all()
        upvotes = reviews.filter(value="up").count()
        ratio = (upvotes / reviews.count()) * 100
        self.vote_total = reviews.count()
        self.vote_ratio = ratio
        self.save()



# text choices value field in Review Model
class VoteTypes(models.TextChoices):
    UP_VOTE = ("up", "Up vote")
    DOWN_VOTE = ("down", "Down vote")


class Review(models.Model):
    review_owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=50, choices=VoteTypes.choices)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, unique=True, editable=False
    )

    class Meta:
        # one profile can have only one review per project
        # unique_together will take care of that
        unique_together = [
            ["review_owner", "project"],
        ]
        ordering = ["-created"]

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
