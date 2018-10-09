from model_mommy import mommy

from ...models import Category_Image


class TestCategoryImage:
    def test_get_random_image_empty(self, db):
        category = mommy.make('Category')
        image = Category_Image.get_random_image(category)
        assert image is None

    def test_get_random_image(self, db):
        category = mommy.make('Category')
        images = [
            mommy.make('Category_Image', category=category)
            for i in range(3)
        ]
        image = Category_Image.get_random_image(category)
        assert image.category == category
        assert image in images
