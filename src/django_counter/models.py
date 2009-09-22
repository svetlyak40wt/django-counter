from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _

class CountManager(models.Manager):
    def get_for_object(self, obj):
        ctype = ContentType.objects.get_for_model(obj)
        return self.get_or_create(content_type=ctype, object_id=obj.id)[0]

    def get_for_model(self, model):
        ctype = ContentType.objects.get_for_model(model)
        return self.filter(content_type=ctype)

    def increment(self, ctype_id, object_id):
        ctype = ContentType.objects.get(id=ctype_id)
        counter, created = self.get_or_create(content_type=ctype, object_id=object_id)
        counter.count += 1
        counter.save()
        return counter

    def inrement_for_object(self, obj):
        counter = self.get_for_object(obj)
        counter.counter += 1
        counter.save()
        return counter

class ViewCounter(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField(_('Object ID'))
    object = generic.GenericForeignKey('content_type', 'object_id')
    count = models.PositiveIntegerField(_('Counter'), default = 0)

    objects = CountManager()

    def get_object_title(self):
        return unicode(self.object)
    get_object_title.short_description = _('Object title')


    def get_content_type(self):
        return self.content_type
    get_content_type.short_description = _('Content type')

    class Meta:
        verbose_name = _('View Counter')
        verbose_name_plural = _('View Counters')
        unique_together = (('content_type', 'object_id'),)
        ordering = ('-count',)

    def __unicode__(self):
        return _(u'Counter for %(object)s = %(count)d') % dict(object = self.object, count = self.count)

class RedirCounter( models.Model ):
    title = models.CharField( _('Title'), max_length = 40, blank=True)
    url = models.CharField(_('Redirect URL'), max_length=255, unique = True)
    count = models.PositiveIntegerField( _('Counter'), default = 0 )

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _('Download Counter')
        verbose_name_plural = _('Download Counters')

class Referer( models.Model ):
    counter = models.ForeignKey(RedirCounter, related_name = 'referers')
    url = models.CharField(_('URL'), max_length = 255)
    count = models.PositiveIntegerField( _('Counter'), default = 0 )
    update_date = models.DateTimeField( editable = False, auto_now = True )

    def __unicode__(self):
        return _(u'To %(counter)s from %(url)s - %(count)s') % dict(
            counter = self.counter, url = self.url, count = self.count)

    class Meta:
        verbose_name = _('Referer')
        verbose_name_plural = _('Referers')
        ordering = ('-update_date',)
        get_latest_by = 'update_date'

