from django import template
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django_counter.models import ViewCounter

def counter(object):
    ctype = ContentType.objects.get_for_model(object)
    return {
        'ctype': ctype,
        'object': object,
        'site': Site.objects.get_current()}

register = template.Library()
register.inclusion_tag('counter/counter.html')(counter)

@register.tag('view_count')
def do_count(parser, token):
    """example: {% view_count for app.model object_id as varname %}"""
    try:
        tag, tmp_for, package, obj, tmp_as, var = token.split_contents()
        if tmp_for != 'for': raise ValueError
        if tmp_as != 'as': raise ValueError
        app, model = package.split('.')
    except ValueError:
        raise template.TemplateSyntaxError, "The valid syntax for view_count tag is: 'view_count for app.model object_id as varname'"
    content_type = ContentType.objects.get(app_label__exact=app, model__exact=model)
    return ViewCountNode(content_type=content_type, obj=obj, var=var)


class ViewCountNode(template.Node):
    def __init__(self, content_type, obj, var):
        self.content_type = content_type
        self.obj = obj
        self.var = var

    def render(self, context):
        if self.obj.isdigit():
            object_id = self.obj
        else:
            try:
                object_id = template.resolve_variable(self.obj, context)
            except template.VariableDoesNotExist:
                return ''
        try:
            count = ViewCounter.objects.get(content_type=self.content_type, object_id=object_id).count
        except ViewCounter.DoesNotExist:
            count = 0
        context[self.var] = count
        return ''
