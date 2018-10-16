from pytest import fixture
from model_mommy import mommy
from ...models import Category


class TestCategory:
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

    def test_get_images_empty(self, setup_category):
        assert not setup_category.get_all_image_header()

    def test_get_images(self, setup_category):
        image = mommy.make('Category_Image', category=setup_category)
        assert setup_category.get_all_image_header()
        assert setup_category.get_all_image_header()[0].description == image.description
