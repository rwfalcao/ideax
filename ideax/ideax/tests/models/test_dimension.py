from model_mommy import mommy
from pytest import fixture
from ...models import Dimension


class TestDimension:
    @fixture
    def dimension(self, db):
        return mommy.make('Dimension')

    def test_created(self, dimension):
        assert dimension.id is not None

    def test_str(self):
        dimension = Dimension(title='Dimensão')
        assert str(dimension) == 'Dimensão'

    def test_title_lenght(self, dimension):
        assert len(dimension.title) <= 200

    def test_description(self, dimension):
        assert isinstance(dimension.description, str)

    def test_description_lenght(self, dimension):
        assert len(dimension.description) <= 500

    def test_weight(self, dimension):
        assert isinstance(dimension.weight, int)

    def test_init_date(self, dimension):
        assert dimension.init_date is not None

    def test_final_date(self, dimension):
        assert dimension.final_date is None
