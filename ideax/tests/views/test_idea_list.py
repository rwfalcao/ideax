from django.contrib.auth.models import AnonymousUser
from model_mommy import mommy
from pytest import fixture

from ideax.views import idea_list


class TestIdeaListView:
    @fixture
    def get_ideas_init(self, mocker):
        return mocker.patch('ideax.views.get_ideas_init')

    @fixture
    def get_phases_count(self, mocker):
        return mocker.patch('ideax.views.get_phases_count')

    def test_idea_list_anonymous(self, rf):
        request = rf.get('/idea/list')
        request.user = AnonymousUser()
        response = idea_list(request)
        assert (response.status_code, response.url) == (302, '/accounts/login/?next=/idea/list')

    def test_idea_list_empty(self, get_ideas_init, get_phases_count, rf, admin_user):
        get_ideas_init.return_value = {
            'ideas': [],
            'challenges': [],
        }
        get_phases_count.return_value = 5
        request = rf.get('/idea/list')
        request.user = admin_user
        response = idea_list(request)
        assert response.status_code == 200
        assert 'Não existem ideias nesta etapa!' in response.content.decode('utf-8', 'strict')

    def test_idea_list(self, get_ideas_init, get_phases_count, rf, admin_user):
        get_ideas_init.return_value = {
            'ideas': [mommy.make('Idea')],
            'challenges': [],
        }
        get_phases_count.return_value = 5
        request = rf.get('/idea/list')
        request.user = admin_user
        response = idea_list(request)
        assert response.status_code == 200
        assert 'Não existem ideias nesta etapa!' not in response.content.decode('utf-8', 'strict')
