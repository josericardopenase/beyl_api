from django.db import models
from utils.models import BaseModel
from ckeditor.fields import RichTextField


# Create your models here.
class Article(BaseModel):
    title = models.CharField(max_length=400)
    texto = RichTextField()
    image = models.ImageField()
    author = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ('-created', )
