import os
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.conf import settings

# utility function for checking for the legal age, and real age
def validate_age(age):
    max_age = 150
    min_age = 10
    if age > max_age:
        raise ValidationError(
            _("Age %(age)s is above the maximum age of %(max_age)s required to register :("),
            params={"age": age, "max_age": max_age},
        )
    if age < min_age:
        raise ValidationError(
            _("Age %(age)s is below the minimum age of %(min_age)s required to register :("),
            params={"age": age, "min_age": min_age},
        )

def images_path():
    return os.path.join(settings.BASE_DIR, "safari_learning/static/course_image")
# Create your models here.



class SafariUser(AbstractUser):
    age = models.PositiveSmallIntegerField(validators=[validate_age])
    profession = models.CharField(max_length=200)

    def __str__(self):
        return "<{0}> {1} {2} {3} is registered".format(self.__class__.__name__, self.id, self.first_name, self.last_name)
    
class SafariCourse(models.Model):
    course_name = models.CharField(max_length=600, default="no course name")
    course_link = models.URLField(max_length=600)
    file_name = models.FilePathField(path=images_path, match=r'\.(jpg|jpeg|png|gif|bmp)$')
    profession_json = models.JSONField()

    def __str__(self):
        return "<{0}> image {1} is saved".format(self.__class__.__name__, self.file_name)