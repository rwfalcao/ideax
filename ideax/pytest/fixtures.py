from pathlib import Path
from pytest import fixture


@fixture
def ideax():
    return 2


@fixture
def test_image(settings):
    image = Path(settings.STATIC_ROOT) / 'images/favico.png'
    with open(image, 'rb') as f:
        return f.read()


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


@fixture(scope='function')
def messages():
    return FakeMessages()
