from ideax.models import Phase


class TestPhase:
    def test_get_phase_by_id(self):
        assert Phase.get_phase_by_id(999) is None
        assert Phase.get_phase_by_id(1) == Phase.GROW

    def test_get_css_class(self):
        assert Phase.get_css_class(999) is None
        assert Phase.get_css_class(8) == Phase.PAUSED
