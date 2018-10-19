from model_mommy import mommy
from pytest import fixture
<<<<<<< HEAD
from model_mommy import mommy
=======

>>>>>>> de304ef8db3345d89b7a9a88f5e88cdd63a2613b
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

<<<<<<< HEAD
    def test_get_images_empty(self, setup_category):
        assert not setup_category.get_all_image_header()

    def test_get_images(self, setup_category):
        image = mommy.make('Category_Image', category=setup_category)
        assert setup_category.get_all_image_header()
        assert setup_category.get_all_image_header()[0].description == image.description
=======
    def test_get_images(self, category):
        mommy.make('Category_Image', category=category)
        assert category.get_all_image_header()
>>>>>>> de304ef8db3345d89b7a9a88f5e88cdd63a2613b
