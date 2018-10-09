import logging
from datetime import date
from pathlib import Path

from pytest import fixture


class FakeMessages:
    ''' mocks the Django message framework, makes it easier to get
    the messages out '''

    def __init__(self):
        self.messages = []

    def add(self, level, message, extra_tags):
        self.messages.append(str(message))

    @property
    def pop(self):
        return self.messages.pop()


class MockDate(date):
    fix_date = date(2010, 1, 1)

    @classmethod
    def today(cls):
        return cls.fix_date


@fixture
def test_image(settings):
    image = Path(settings.STATIC_ROOT) / 'images/favico.png'
    with open(image, 'rb') as f:
        return f.read()


@fixture(scope='function')
def messages():
    return FakeMessages()


@fixture
def debug():
    return logging.warn


@fixture
def mock_today():
    return MockDate
