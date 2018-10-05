from django.contrib.auth.models import AnonymousUser
from model_mommy import mommy
from pytest import fixture

from ideax.views import accept_use_term, idea_list, index


class TestIndexView:
    def test_index_anonymous(self, rf, debug):
        request = rf.get('/')
        request.user = AnonymousUser()
        response = index(request)
        assert response.status_code == 200
        # TODO: It seems malformed HTML
        debug(response.content.decode('utf8'))
        assert 'class="login-button"' in response.content.decode('utf-8', 'strict')

    def test_index(self, rf, admin_user):
        request = rf.get('/')
        request.user = admin_user
        response = index(request)
        assert response.status_code == 200
        # TODO: Enhance test
        assert '<title>Ideia X </title>' in response.content.decode('utf-8', 'strict')


class TestAcceptUseTermView:
    def test_accept_use_term_anonymous(self, rf):
        request = rf.get('/term/accept')
        request.user = AnonymousUser()
        response = accept_use_term(request)
        assert (response.status_code, response.url) == (302, '/accounts/login/?next=/term/accept')

    def test_accept_use_term_not_accepted(self, rf, admin_user, messages, get_ip):
        admin_user.userprofile.use_term_accept = False
        request = rf.get('/term/accept')
        request.user = admin_user
        request._messages = messages
        response = accept_use_term(request)
        assert (response.status_code, response.url) == (302, '/')
        assert messages.messages == ['Termo de uso aceito!']
        get_ip.assert_called_once_with(request)

    def test_accept_use_term_accepted(self, rf, admin_user, messages):
        admin_user.userprofile.use_term_accept = True
        request = rf.get('/term/accept')
        request.user = admin_user
        request._messages = messages
        response = accept_use_term(request)
        assert (response.status_code, response.url) == (302, '/')
        assert messages.messages == ['Termo de uso já aceito!']


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

    def test_idea_list_empty(self, get_ideas_init, get_phases_count, rf, admin_user, mocker):
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

    def test_idea_list(self, get_ideas_init, get_phases_count, rf, admin_user, mocker):
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
