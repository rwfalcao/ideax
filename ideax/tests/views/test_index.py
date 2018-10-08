from django.contrib.auth.models import AnonymousUser

import ideax.views
from ideax.views import index


class TestIndexView:
    def test_index_anonymous(self, rf, debug):
        request = rf.get('/')
        request.user = AnonymousUser()
        response = index(request)
        assert response.status_code == 200
        # TODO: It seems malformed HTML
        debug(response.content.decode('utf8'))
        assert 'class="login-button"' in response.content.decode('utf-8', 'strict')

    def test_index(self, rf, admin_user, mocker):
        ideax.views.audit = mocker.Mock()
        request = rf.get('/')
        request.user = admin_user
        response = index(request)
        assert response.status_code == 200
        # TODO: Enhance test
        assert '<title>Ideia X </title>' in response.content.decode('utf-8', 'strict')
