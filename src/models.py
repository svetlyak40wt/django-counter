from django.db import models
from django.utils.translation import ugettext_lazy as _

class TestModel( models.Model ):
    name = models.CharField( _('Title'), max_length = 40, blank=True)

    class Meta:
        verbose_name = _('Test model')
        verbose_name_plural = _('Test models')

