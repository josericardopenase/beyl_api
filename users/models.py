"""Users module"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from utils.models import BaseModel
from datetime import date
from django.utils.timezone import now
from datetime import date
from PIL import Image 
from io import BytesIO
from django.core.files import File

# Create your models here.

class _Image(Image.Image):

    def crop_to_aspect(self, aspect, divisor=1, alignx=0.5, aligny=0.5):
        """Crops an image to a given aspect ratio.
        Args:
            aspect (float): The desired aspect ratio.
            divisor (float): Optional divisor. Allows passing in (w, h) pair as the first two arguments.
            alignx (float): Horizontal crop alignment from 0 (left) to 1 (right)
            aligny (float): Vertical crop alignment from 0 (left) to 1 (right)
        Returns:
            Image: The cropped Image object.
        """
        if self.width / self.height > aspect / divisor:
            newwidth = int(self.height * (aspect / divisor))
            newheight = self.height
        else:
            newwidth = self.width
            newheight = int(self.width / (aspect / divisor))
        img = self.crop((alignx * (self.width - newwidth),
                         aligny * (self.height - newheight),
                         alignx * (self.width - newwidth) + newwidth,
                         aligny * (self.height - newheight) + newheight))
        return img

Image.Image.crop_to_aspect = _Image.crop_to_aspect

class CustomUser(AbstractUser, BaseModel):

    """
    CustomUser():

    Custom user to select between beeing trainer or
    athlete.

    """

    USER_TYPES = [ 
        ('Athlete', 'ATH'),
        ('Trainer', 'TRA'),
    ]

    user_type = models.CharField( 
        'Type of users', 
        help_text='Defines if the user is a athlete or a trainer', 
        choices=USER_TYPES,
        default='Athlete',
        max_length=10, 
        blank=False)

    USERNAME_FIELD = 'email'

    is_verified = models.BooleanField("User verified", default=False,
                                      help_text="Have user confirmed hes email?")
    email = models.EmailField('email address', blank=False, unique=True)
    profile_pic = models.ImageField(blank=False, default='profile.png', verbose_name=("Profile_pic"))
    first_name = models.CharField(blank=False, max_length=58)
    last_name = models.CharField(blank=False, max_length=58)
    username = models.CharField(blank=True, null=True, max_length=50)
    REQUIRED_FIELDS = []

    def compress(self, image):
        im = Image.open(image)
        # create a BytesIO object
        im_io = BytesIO() 
        im = im.crop_to_aspect(300, 300)
        im = im.resize((500, 500))
        # save image to BytesIO object
        im.save(im_io, 'JPEG', quality=70, optimize=True) 
        # create a django-friendly Files object
        new_image = File(im_io, name=image.name)

        return new_image

    def save(self, *args, **kwargs):
        # Did we have to resize the image?
        # We pop it to remove from kwargs when we pass these along
        new_image = self.compress(self.profile_pic)
        # set self.image to new_image
        self.profile_pic = new_image
        # save
        super(CustomUser, self).save(*args, **kwargs)




class TrainerPlan(BaseModel):
    user_count = models.PositiveIntegerField(null = False, blank= False)
    price = models.PositiveIntegerField(null = False, blank= False)
    name = models.CharField(max_length=200)

class TrainerUser(BaseModel):

    """
    TrainerUser():

    Saves the relationship between CustomUser (out base user)
    and a trainer.

    """

    user = models.ForeignKey(CustomUser, related_name='trainer_user', on_delete=models.CASCADE)
    plan = models.ForeignKey(TrainerPlan, related_name = 'trainer_plan', on_delete = models.CASCADE, default=1)


    def __str__(self):
        return self.user.email


class AthleteUser(BaseModel):

    """
    AthleteUser():

    Saves the relationship between CustomUser (out base user)
    and a athlete.

    """
    
    SEX_CHOICES = ( 
        ('hombre','H'), 
        ('mujer','M'),
    )

    SPORT_AMOUNT = ( 
        ('ne','NE'), 
        ('el','EL'), 
        ('em','EM'),
        ('ef','EF'),
        ('emf','EMF'),
    )

    user = models.ForeignKey(CustomUser, related_name='athlete_user', on_delete=models.CASCADE)
    trainer = models.ForeignKey(TrainerUser, related_name='athlete_trainer',
                                     on_delete=models.CASCADE, null=True, blank=True)

    #===================
     #  User training
    #===================

    rutine = models.OneToOneField('trainings.Rutine', related_name='user_rutine',
                                on_delete=models.SET_NULL, help_text="Rutine of the user", blank=True, null=True)
    diet = models.OneToOneField('trainings.Diet', related_name='user_diet', on_delete=models.SET_NULL,
                                help_text="Diet of the user", blank=True, null=True)

    trainer_rutine = models.OneToOneField('trainings.Rutine', related_name='trainer_rutine',
                                on_delete=models.CASCADE, help_text="Rutine of the user", blank=True, null=True)
    trainer_diet = models.OneToOneField('trainings.Diet', related_name='trainer_diet', on_delete=models.CASCADE,
                                help_text="Diet of the user", blank=True, null=True)

    weight = models.FloatField('weight', help_text="Weight of the user in Kg")
    height = models.FloatField('height', help_text="Hieght of the user in Cm")
    fat = models.FloatField('fat_percent', help_text="Fat in percentage")
    born_date = models.DateField()
    sexo = models.CharField('sex_choices', help_text="Choices of sex", choices=SEX_CHOICES, max_length=8)
    amount_excersise = models.CharField('amount_excersise', help_text="Choices of sport activity ", choices=SPORT_AMOUNT , max_length=80, default=SPORT_AMOUNT[0][1])
    alergias = models.TextField(null=True, blank=True)


    @property 
    def age(self):
        today = date.today()
        return today.year - self.born_date.year - ((today.month, today.day) < (self.born_date.month, self.born_date.day))

    def __str__(self):
        return self.user.email
