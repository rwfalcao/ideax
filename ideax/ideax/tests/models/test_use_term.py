from datetime import datetime

from django.utils import timezone

from model_mommy import mommy


class TestUseTerm:
    def test_is_past_due(self, db):
        use_term = mommy.make('Use_Term')
        assert not use_term.is_past_due

    def test_is_past_due_future(self, db):
        # TODO: Evaluate use of timezone
        use_term = mommy.make('Use_Term', final_date=timezone.make_aware(datetime(2099, 12, 31)))
        assert use_term.is_past_due

    def test_valid_date(self, db):
        use_term = mommy.make(
            'Use_Term',
            init_date=timezone.make_aware(datetime(2018, 1, 1)),
            final_date=timezone.make_aware(datetime(2018, 12, 31)),
        )
        assert not use_term.is_invalid_date()

    def test_invalid_date(self, db):
        use_term = mommy.make(
            'Use_Term',
            init_date=timezone.make_aware(datetime(2019, 1, 1)),
            final_date=timezone.make_aware(datetime(2018, 12, 31)),
        )
        assert use_term.is_invalid_date()
