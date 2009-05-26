from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.test import TestCase, Client
from django.core.urlresolvers import reverse

from pdb import set_trace

from models import ViewCounter

class Post(models.Model):
    title = models.CharField('Title', max_length = 100)

class SimpleTests(TestCase):
    def setUp(self):
        self.ctype = ContentType.objects.get_for_model(Post)
        self.post = Post(title='Blah minor')
        self.post.save()
        super(SimpleTests, self).setUp()

    def tearDown(self):
        Post.objects.all().delete()
        super(SimpleTests, self).tearDown()

    def testForCounterIncrement(self):
        client = Client()

        counter = ViewCounter.objects.get_for_object(self.post)
        self.assertEqual(0, counter.counter)

        response = client.get(
            reverse('django-counter-count', kwargs = dict(
                ctype_id=self.ctype.id, object_id=self.post.id)))
        self.assertEqual(200, response.status_code)

        counter = ViewCounter.objects.get_for_object(self.post)
        self.assertEqual(1, counter.counter)
