""" Django beyl utilities """

from django.db import models

class BaseModel(models.Model):

    """

    Abstract class that makes herency from other classes
    in the django app

    """

    created = models.DateTimeField(
        'created at',
        auto_now_add=True,
        help_text="Date time on which the object was created"
    )

    modified = models.DateTimeField(
        'Modified at',
        auto_now=True,
        help_text='Date time on which the object was modified'
    )


    class Meta:

        abstract = True
        get_latest_by = 'created'
        ordering = ['-created', '-modified']