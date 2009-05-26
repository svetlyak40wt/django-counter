from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.test import TestCase, Client
from django.core.urlresolvers import reverse

from pdb import set_trace

from models import *

class Post(models.Model):
    title = models.CharField('Title', max_length = 100)

class CounterTests(TestCase):
    def setUp(self):
        self.ctype = ContentType.objects.get_for_model(Post)
        self.post = Post(title='Blah minor')
        self.post.save()
        super(CounterTests, self).setUp()

    def tearDown(self):
        Post.objects.all().delete()
        super(CounterTests, self).tearDown()

    def testForCounterIncrement(self):
        client = Client()

        counter = ViewCounter.objects.get_for_object(self.post)
        self.assertEqual(0, counter.count)

        response = client.get(
            reverse('django-counter-count', kwargs = dict(
                ctype_id=self.ctype.id, object_id=self.post.id)))
        self.assertEqual(200, response.status_code)

        counter = ViewCounter.objects.get_for_object(self.post)
        self.assertEqual(1, counter.count)

class RedirTests(TestCase):
    def setUp(self):
        super(RedirTests, self).setUp()

    def testRedirByIdFailIfCounterNotExists(self):
        client = Client()

        response = client.get(
            reverse('django-counter-redir', kwargs = dict(
                counter_id=123)))
        self.assertEqual(404, response.status_code)

    def testExistingRedir(self):
        client = Client()

        url = 'http://aartemenko.com'
        counter = RedirCounter(url = url)
        counter.save()

        response = client.get(
            reverse('django-counter-redir', kwargs = dict(
                counter_id=counter.id)),
            follow = False)
        self.assertEqual(302, response.status_code)
        self.assertEqual(url, response['Location'])

        counter = RedirCounter.objects.get(url = url)
        self.assertEqual(1, counter.count)

