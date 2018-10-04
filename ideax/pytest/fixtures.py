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
