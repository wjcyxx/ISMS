from django.db import models
import uuid
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.

@python_2_unicode_compatible

class User(models.Model):



    class Meta:
        db_table = "T_User"
