from ideax.forms import CategoryForm


class TestCategoryForm(object):
    def test_valid(self):
        data = {
            'title': 'Mobile',
            'description': 'Mobile interface',
        }
        form = CategoryForm(data)
        assert form.is_valid()

    def test_invalid(self, snapshot):
        data = {}
        form = CategoryForm(data)
        assert not form.is_valid()
        assert len(form.errors) == 2
        snapshot.assert_match(form.errors)
