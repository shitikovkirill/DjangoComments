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

    user = models.ForeignKey(
        get_user_model(), on_delete=models.PROTECT, related_name="author"
    )

    def __str__(self):
        return self.title


class Attachment(models.Model):
    file = models.FileField()
    name = models.CharField(max_length=100)
    version = models.IntegerField(default=0)
    upload_date = models.DateTimeField(auto_now=True, db_index=True)
    owner = models.ForeignKey(
        get_user_model(), on_delete=models.PROTECT, related_name="uploaded_files"
    )
    post = models.ForeignKey(
        Post, on_delete=models.PROTECT, related_name="uploaded_files"
    )
    size = models.IntegerField(default=0)
