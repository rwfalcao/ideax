from model_mommy import mommy
from pytest import fixture

from ...models import Category


class TestCategory:
    @fixture
    def category(self, db):
        return mommy.make('Category')

    def test_created(self, category):
        assert category.id is not None

    def test_str(self):
        category = Category(title='Mobile')
        assert str(category) == 'Mobile'

    def test_get_images_empty(self, category):
        assert not category.get_all_image_header()

    def test_get_images(self, category):
        mommy.make('Category_Image', category=category)
        assert category.get_all_image_header()
