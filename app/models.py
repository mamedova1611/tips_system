from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

class Profile(models.Model):
    login = models.CharField(max_length=11, verbose_name=_("номер телефона"))
    fio = models.CharField(max_length=50, null=True, blank=True, verbose_name=_("ФИО"))
    city = models.CharField(max_length=30, null=True, blank=True, verbose_name=_('город'))
    foto = models.ImageField(upload_to='foto/', blank=True,null=True, verbose_name=_('изображение'))
    job =models.CharField(max_length=30, null=True, blank=True, verbose_name=_('должность'))
    balance = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('баланс'))