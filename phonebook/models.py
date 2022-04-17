from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

validator = RegexValidator(regex="^0[0-9]{2,}[0-9]{7,}$", message="invalid phone number")
# Create your models here.
class PhoneBook(models.Model):
    phone_number = models.CharField(max_length=11, verbose_name=_("phonenumber"))
    first_name = models.CharField(max_length=20, verbose_name=_("firstname"))
    last_name = models.CharField(max_length=20, verbose_name=_("lastname"))
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        unique_together = ["phone_number", "user"]
