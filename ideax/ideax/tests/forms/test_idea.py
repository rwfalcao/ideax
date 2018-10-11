from model_mommy import mommy
from pytest import fixture

from ....users.models import UserProfile
from ...forms import IdeaForm


class TestIdeaForm:
    @fixture
    def authors(self):
        # TODO: Perthaps queryset should have a default value
        return UserProfile.objects.all()

    def test_invalid(self, authors, snapshot):
        form = IdeaForm({}, authors=authors)
        assert not form.is_valid()
        assert len(form.errors) == 6
        snapshot.assert_match(form.errors)

    def test_valid(self, authors, db):
        category = mommy.make('Category')
        data = {
            'title': 'Super idea',
            'summary': 'It will change the entire world',
            'target': 'people around the world',
            'solution': 'all the problems',
            'oportunity': 'all the time',
            'category': category.id,
        }
        form = IdeaForm(data, authors=authors)
        assert form.is_valid()
