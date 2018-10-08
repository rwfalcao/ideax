import json
from datetime import datetime, timedelta

from model_mommy import mommy

import ideax.views
from ideax.views import (get_category_list, get_phases, get_term_of_user,
                         get_use_term_list)


class TestNonMiscView:
    """Test for non view functions in ideax.views (for refactor)"""
    def test_get_phases(self, snapshot):
        phases = get_phases()
        assert len(phases.keys()) == 1
        # TODO: why str is necessary?
        cleaned = [(k, str(v)) for k, v in phases['phases']]
        snapshot.assert_match(cleaned)

    def test_get_category_list(self, db, debug):
        category = mommy.make('Category')
        categories = get_category_list()
        assert list(categories.keys()) == ['category_list']
        assert categories['category_list'].last() == category

    def test_get_term_of_user_empty(self, rf, db, debug):
        request = rf.get('/')
        response = get_term_of_user(request)
        assert response.status_code == 200
        assert json.loads(response.content) == {'term': 'Termo de Uso não encontrado'}

    def test_get_term_of_user(self, rf, db, debug):
        mommy.make('Use_Term', term='EULA Test', final_date=datetime.now() + timedelta(days=1))
        request = rf.get('/')
        response = get_term_of_user(request)
        assert response.status_code == 200
        assert json.loads(response.content) == {'term': 'EULA Test'}

    def test_get_use_term_list(self, db, mock_today):
        ideax.views.date = mock_today
        response = get_use_term_list()
        assert len(response['use_term_list']) == 1
        assert response['use_term_list'][0].term == 'A generic Term of Use.'
        assert response['today'] == mock_today.fix_date

# get_valid_use_term, get_featured_challenges
# file_upload, idea_search, get_authors
