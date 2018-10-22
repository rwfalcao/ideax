from django.db.utils import DataError

from model_mommy import mommy
from pytest import mark, raises

from ...models import Idea


class TestIdea:
    @mark.skip('TODO: Missing PhaseHistory empty')
    def test_get_current_phase_history_empty(self, db):
        idea = mommy.make('Idea')
        assert idea.get_current_phase_history() is None

    def test_get_current_phase_history(self, db):
        idea = mommy.make('Idea')
        ph = mommy.make('Phase_History', idea=idea, current=True)
        assert idea.get_current_phase_history() == ph

    def test_get_absolute_url(self):
        idea = Idea(id=999)
        assert idea.get_absolute_url() == '/idea/999/'

    def test_get_approval_rate_zero(self, db):
        idea = mommy.make('Idea')
        assert idea.get_approval_rate() == 0

    def test_get_approval_rate(self, db):
        idea = mommy.make('Idea')
        mommy.make('Popular_Vote', idea=idea, like=True)
        mommy.make('Popular_Vote', idea=idea, like=False)
        assert idea.get_approval_rate() == 50

    @mark.skip("TODO: Longtext (mysql) doesn't have size")
    def test_max_length_summary(self, db):
        # Success
        mommy.make('Idea', summary='X' * 140)

        # Fail
        with raises(DataError):
            mommy.make('Idea', summary='X' * 141)
