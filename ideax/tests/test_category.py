from pytest import fixture
from ideax.models import Category


class TestCategory(object):
    @fixture
    def setup_category(self, db):
        c = Category()
        c.title = 'Mobile'
        c.description = 'Mobile interface for existing service'
        c.save()
        return c

    def test_created(self, setup_category):
        assert setup_category.id is not None

    def test_str(self, setup_category):
        assert str(setup_category) == setup_category.title

    def test_get_images(self, setup_category):
        # TODO: Test with images created
        assert len(setup_category.get_all_image_header()) == 0

