from django.db import models
from django.contrib.auth import get_user_model


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Post(TimeStampedModel):
    title = models.CharField(max_length=200)
    description = models.TextField()
    file = models.FileField()

    user = models.ForeignKey(
        get_user_model(), on_delete=models.PROTECT, related_name="author"
    )

    def __str__(self):
        return self.title

