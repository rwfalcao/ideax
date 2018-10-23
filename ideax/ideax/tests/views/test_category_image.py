from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import PermissionDenied
from django.http.response import Http404

from pytest import raises

from ...views import (category_image_edit, category_image_remove)


class TestCategoryImageEdit:
    def test_anonymous(self, rf):
        request = rf.get(f'/categoryimage/99999/edit/')
        request.user = AnonymousUser()
        response = category_image_edit(request, 99999)
        assert (response.status_code, response.url) == (302, '/accounts/login/?next=/categoryimage/99999/edit/')

    def test_not_found(self, rf, admin_user):
        request = rf.get(f'/categoryimage/99999/edit/')
        request.user = admin_user
        with raises(Http404):
            category_image_edit(request, 99999)

    def test_get_common_user(self, rf, common_user):
        request = rf.get('/categoryimage/1/edit/')
        request.user = common_user
        with raises(PermissionDenied):
            category_image_edit(request, 1)


class TestCategoryImageRemove:
    def test_anonymous(self, rf):
        request = rf.get('/')
        request.user = AnonymousUser()
        response = category_image_remove(request, 999)
        assert (response.status_code, response.url) == (302, '/accounts/login/?next=/')

    def test_common_user(self, rf, common_user):
        request = rf.get('/')
        request.user = common_user
        with raises(PermissionDenied):
            category_image_remove(request, 1)
