from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import PermissionDenied
from django.http.response import Http404

from pytest import raises

from ...models import Dimension
from ...views.dimension import DimensionHelper, dimension_edit, dimension_list, dimension_new, dimension_remove


class TestDimensionNew:
    def test_anonymous(self, rf):
        request = rf.get('/')
        request.user = AnonymousUser()
        response = dimension_new(request)
        assert (response.status_code, response.url) == (302, '/accounts/login/?next=/')

    def test_permission_denied(self, rf, common_user):
        request = rf.get('/')
        request.user = common_user
        with raises(PermissionDenied):
            dimension_new(request)

    def test_get(self, rf, factory_user, mocker):
        render = mocker.patch('ideax.ideax.views.dimension.render')
        form = mocker.patch('ideax.ideax.views.dimension.DimensionForm')

        request = rf.get('/')
        request.user = factory_user('ideax.add_dimension')

        dimension_new(request)
        form.assert_called_once()
        render.assert_called_once_with(request, 'ideax/dimension_new.html', {'form': form.return_value})

    def test_post(self, rf, factory_user, mocker, messages):
        audit = mocker.patch('ideax.ideax.views.dimension.audit')
        form = mocker.patch('ideax.ideax.views.dimension.DimensionForm')
        form.return_value.is_valid.return_value = True
        user_profile = mocker.patch('ideax.users.models.UserProfile.objects')
        user_profile.get.return_value = None

        request = rf.post('/', {})
        request.user = factory_user('ideax.add_dimension')
        request._messages = messages

        response = dimension_new(request)
        form.assert_called_once_with(request.POST)
        audit.assert_called_once()
        assert (response.status_code, response.url) == (302, '/dimension/')
        assert messages.isSuccess
        assert messages.messages == ['Dimension saved successfully!']

    def test_post_invalid_form(self, rf, factory_user, mocker):
        form = mocker.patch('ideax.ideax.views.dimension.DimensionForm')
        form.return_value.is_valid.return_value = False
        user_profile = mocker.patch('ideax.users.models.UserProfile.objects')
        user_profile.get.return_value = None

        request = rf.post('/', {})
        request.user = factory_user('ideax.add_dimension')

        response = dimension_new(request)
        assert response.status_code == 200


class TestDimensionEdit:
    def test_anonymous(self, rf):
        request = rf.get(f'/dimension/99999/edit/')
        request.user = AnonymousUser()
        response = dimension_edit(request, 99999)
        assert (response.status_code, response.url) == (302, '/accounts/login/?next=/dimension/99999/edit/')

    def test_not_found(self, rf, factory_user, db):
        request = rf.get(f'/dimension/99999/edit/')
        request.user = factory_user('ideax.change_dimension')
        with raises(Http404):
            dimension_edit(request, 99999)

    def test_get_common_user(self, rf, common_user):
        request = rf.get('/dimension/1/edit/')
        request.user = common_user
        with raises(PermissionDenied):
            dimension_edit(request, 1)

    def test_get(self, rf, factory_user, mocker):
        get = mocker.patch('ideax.ideax.views.dimension.get_object_or_404')
        render = mocker.patch('ideax.ideax.views.dimension.render')
        form = mocker.patch('ideax.ideax.views.dimension.DimensionForm')

        request = rf.get(f'/dimension/55/edit/')
        request.user = factory_user('ideax.change_dimension')
        dimension_edit(request, 55)

        get.assert_called_once_with(Dimension, pk=55)
        render.assert_called_once_with(request, 'ideax/dimension_edit.html', {'form': form.return_value})

    def test_post(self, rf, factory_user, mocker, messages):
        get = mocker.patch('ideax.ideax.views.dimension.get_object_or_404')
        mocker.patch('ideax.ideax.views.dimension.audit')
        dimension_form = mocker.patch('ideax.ideax.views.dimension.DimensionForm')
        dimension_form.return_value.is_valid.return_value = True

        request = rf.post(f'/dimension/55/edit/', {})
        request.user = factory_user('ideax.change_dimension')
        request._messages = messages
        response = dimension_edit(request, 55)

        get.assert_called_once_with(Dimension, pk=55)
        dimension_form.assert_called_once_with(request.POST, instance=get.return_value)
        assert (response.status_code, response.url) == (302, '/dimension/')
        assert messages.isSuccess
        assert messages.messages == ['Dimension changed successfully!']

    def test_post_invalid_form(self, rf, factory_user, mocker, messages):
        get = mocker.patch('ideax.ideax.views.dimension.get_object_or_404')
        mocker.patch('ideax.ideax.views.dimension.audit')
        dimension_form = mocker.patch('ideax.ideax.views.dimension.DimensionForm')
        dimension_form.return_value.is_valid.return_value = False
        render = mocker.patch('ideax.ideax.views.dimension.render')

        request = rf.post(f'/dimension/55/edit/', {})
        request.user = factory_user('ideax.change_dimension')
        request._messages = messages
        dimension_edit(request, 55)

        get.assert_called_once_with(Dimension, pk=55)
        dimension_form.assert_called_once_with(request.POST, instance=get.return_value)
        # TODO: any fail message?
        render.assert_called_once_with(request, 'ideax/dimension_edit.html', {'form': dimension_form.return_value})


class TestDimensionRemove:
    def test_anonymous(self, rf):
        request = rf.get('/')
        request.user = AnonymousUser()
        response = dimension_remove(request, 999)
        assert (response.status_code, response.url) == (302, '/accounts/login/?next=/')

    def test_common_user(self, rf, common_user):
        request = rf.get('/')
        request.user = common_user
        with raises(PermissionDenied):
            dimension_remove(request, 1)

    def test_get(self, rf, factory_user, mocker, messages):
        audit = mocker.patch('ideax.ideax.views.dimension.audit')
        get = mocker.patch('ideax.ideax.views.dimension.get_object_or_404')
        DimensionHelper = mocker.patch('ideax.ideax.views.dimension.DimensionHelper')
        DimensionHelper.get_dimension_list.return_value = {}
        dimension = mocker.patch('ideax.ideax.views.dimension.Dimension')
        dimension.__name__ = 'Dimension'

        request = rf.get('/')
        request.user = factory_user('ideax.delete_dimension')
        request._messages = messages
        response = dimension_remove(request, 999)

        get.assert_called_once_with(dimension, pk=999)
        audit.assert_called_once()
        assert (response.status_code, response.url) == (302, '/dimension/')
        assert messages.isSuccess
        assert messages.messages == ['Dimension removed successfully!']


class TestDimensionList:
    def test_anonymous(self, rf):
        request = rf.get('/')
        request.user = AnonymousUser()
        response = dimension_list(request)
        assert (response.status_code, response.url) == (302, '/accounts/login/?next=/')

    def test_get(self, rf, mocker, common_user):
        mocker.patch('ideax.ideax.views.dimension.audit')
        DimensionHelper = mocker.patch('ideax.ideax.views.dimension.DimensionHelper')
        DimensionHelper.get_dimension_list.return_value = {}
        render = mocker.patch('ideax.ideax.views.dimension.render')

        request = rf.get('/')
        request.user = common_user
        dimension_list(request)

        render.assert_called_once_with(request, 'ideax/dimension_list.html', {})


class TestDimensionHelper:
    def test_get_dimension_list(self, mocker):
        objects = mocker.patch('ideax.ideax.views.dimension.Dimension.objects')
        objects.all.return_value = []

        result = DimensionHelper.get_dimension_list()

        assert result == {'dimension_list': []}
