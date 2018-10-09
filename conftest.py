from pytest import fixture
from django.core.management import call_command


pytest_plugins = [
    'ideax.tests.fixtures',
    'ideax.ideax.tests.fixtures',
]


@fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command('loaddata', 'docker/initialdata.json')
