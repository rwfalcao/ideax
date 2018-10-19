from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import PermissionDenied
from pytest import raises

from ...views import category_new


class TestCategoryNew:
    def test_anonymous(self, rf):
        request = rf.get('/')
        request.user = AnonymousUser()
        response = category_new(request)
        assert (response.status_code, response.url) == (302, '/accounts/login/?next=/')

    def test_permission_denied(self, rf, common_user):
        request = rf.get('/')
        request.user = common_user
        with raises(PermissionDenied):
            category_new(request)

    def test_get(self, rf, factory_user, mocker):
        render = mocker.patch('ideax.ideax.views.render')
        form = mocker.patch('ideax.ideax.views.CategoryForm')

        request = rf.get('/')
        request.user = factory_user('ideax.add_category')

        category_new(request)
        form.assert_called_once()
        render.assert_called_once_with(request, 'ideax/category_new.html', {'form': form.return_value})

    def test_post(self, rf, factory_user, mocker, messages):
        form = mocker.patch('ideax.ideax.views.CategoryForm')
        form.return_value.is_valid.return_value = True
        user_profile = mocker.patch('ideax.users.models.UserProfile.objects')
        user_profile.get.return_value = None

        request = rf.post('/', {})
        request.user = factory_user('ideax.add_category')
        request._messages = messages

        response = category_new(request)
        form.assert_called_once_with(request.POST)
        assert (response.status_code, response.url) == (302, '/category/list/')
        assert messages.isSuccess
        assert messages.messages == ['Category saved successfully!']

    def test_post_invalid_form(self, rf, factory_user, mocker):
        form = mocker.patch('ideax.ideax.views.CategoryForm')
        form.return_value.is_valid.return_value = False
        user_profile = mocker.patch('ideax.users.models.UserProfile.objects')
        user_profile.get.return_value = None

        request = rf.post('/', {})
        request.user = factory_user('ideax.add_category')

        response = category_new(request)
        # TODO: Maybe a message
        assert response.status_code == 200
