from pytest import fixture

from .. import views


@fixture
def get_ip(ideax_views, mocker):
    patch = mocker.patch.object(ideax_views, 'get_ip')
    patch.return_value = '1.1.1.1'
    return patch


@fixture
def ideax_views():
    return views
