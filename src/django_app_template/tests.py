from unittest import TestCase

class SimpleTests(TestCase):
    def testForFail(self):
        self.assert_(False and 'Please, fix me.')
