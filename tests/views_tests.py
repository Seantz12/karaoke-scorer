import unittest
import views


class ViewsTests(unittest.TestCase):
    """Unit tests for views (app routes)."""

    def test_main(self):
        """Test the `main` view."""
        self.assertEqual(views.main(), "Don't visit here!")
