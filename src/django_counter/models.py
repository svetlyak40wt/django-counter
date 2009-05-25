from django.db import models
from firefly.utils.functions import now
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _

class CountManager(models.Manager):
    def get_for_object(self, obj):
        ctype = ContentType.objects.get_for_model(obj)
        return self.get_or_create(content_type=ctype, object_id=obj.id)

    def get_for_model(self, model):
        ctype = ContentType.objects.get_for_model(model)
        return self.filter(content_type=ctype)

    def increment(self, ctype_id, object_id):
        ctype = ContentType.objects.get(id=ctype_id)
        counter,created = self.get_or_create(content_type=ctype, object_id=object_id)
        counter.counter += 1
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
    counter = models.PositiveIntegerField(_('Counter'), default = 0)

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
        ordering = ('-counter',)

    class Admin:
        list_display = ('get_object_title', 'get_content_type', 'counter')
        list_filter = ('content_type',)

    def __unicode__(self):
        return _('Counter for %(object)s = %(counter)d') % (self.object, self.counter)

class DownloadCounter( models.Model ):
    title = models.CharField( _('Title'), max_length = 40, blank=True)
    redir_url = models.CharField(_('Redirect URL'), max_length=255)
    cnt = models.PositiveIntegerField( _('Counter'), default = 0 )

    def __unicode__(self):
        return self.title

    class Admin:
        list_display = ('id', 'title', 'redir_url', 'cnt')
        list_display_links =  list_display

    class Meta:
        verbose_name = _('Download Counter')
        verbose_name_plural = _('Download Counters')

class Referer( models.Model ):
    counter = models.ForeignKey(DownloadCounter)
    url = models.CharField(_('URL'), max_length = 255)
    cnt = models.PositiveIntegerField( _('Counter'), default = 0 )
    update_date = models.DateTimeField( editable = False, auto_now = True )

    def __unicode__(self):
        return u'To %s from %s - %s' % (self.counter, self.url, self.cnt)

    class Admin:
        list_display = ('id', 'counter', 'url', 'cnt', 'update_date')
        date_hierarchy = 'update_date'
        list_filter = ('update_date',)

    class Meta:
        verbose_name = _('Referer')
        verbose_name_plural = _('Referers')
        ordering = ('-update_date',)
        get_latest_by = 'update_date'
