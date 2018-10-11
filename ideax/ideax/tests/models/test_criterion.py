from model_mommy import mommy


class TestCriterion:
    def test_str(self, db):
        criterion = mommy.make('Criterion', description='Test criterion')
        assert str(criterion) == criterion.description
