from django.test import TestCase

class BasicTest(TestCase):
    def test_passes_always(self):
        self.assertTrue(True)