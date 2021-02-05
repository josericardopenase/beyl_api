""" Django beyl utilities """

from django.db import models
from decimal import *

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

class OrderedModelManager(models.Manager):
    """
    
    Handles custom implementation of orderering a model.

    """

    def create_ordered(self, queryset ,*args, **kwargs):
        """

            Sets the order according to the last element when
            is added.

        """

        factor = 1

        try:
           kwargs['order'] = queryset.last().order + 1 
        except:
            kwargs['order'] = 1

        instance = self.model(**kwargs)

        return super(OrderedModelManager, self).create(*args, **kwargs)

class OrderedModel(BaseModel):

    """

    Abstract class that makes ordered 
    model in django.

    """

    objects = OrderedModelManager()
    order = models.BigIntegerField(blank=True)

    class Meta:

        """
        
        We make the class abstract and set a default 
        ordering.

        """

        abstract = True
        get_latest_by = ['-order',]
        ordering = ('order',)



    def move_to(self, queryset, index):

        """

        Move a element to a concrete position
        of the list in the queryset

        """

        from_index = self.order
        to_index = index
        from_obj = self

        last_order =  queryset.last().order
        first_order =  queryset.first().order

        if to_index  > last_order:
            to_index = last_order

        if to_index < first_order:
            to_index = first_order


        if abs(to_index - from_index) == 1:

            """

                If the items are consecutive
                we can use 0(1) transformation

            """

            from_obj.order = to_index
            
            to_obj = queryset.get(order = to_index)
            to_obj.order = from_index

            to_obj.save()

        else:
            """

            if you are ordering inside other elements 
            we need to modify the list with a 0(n) algorithm

            """

            from_obj.order = to_index
            
            if(to_index - from_index < 0):
                """

                    You are going upside

                """

                for x in queryset.filter(order__gte = to_index):
                    x.order += 1
                    x.save()

            else:
                """
                    You are going downside
                """
                for x in queryset.filter(order__lte = to_index):
                    x.order -= 1
                    x.save()

        from_obj.save()




