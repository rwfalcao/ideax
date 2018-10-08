import json
from datetime import datetime, timedelta
from itertools import product

from django.db.models import QuerySet
from model_mommy import mommy

import ideax.views
from ideax.views import (get_authors, get_category_list,
                         get_featured_challenges, get_phases, get_term_of_user,
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

    def test_get_featured_challenges_empty(self, db):
        response = get_featured_challenges()
        assert isinstance(response, QuerySet)
        assert response.count() == 0

    def test_get_featured_challenges(self, db):
        challenges = {
            (active, discarted): mommy.make('Challenge', active=active, discarted=discarted)
            for active, discarted in product((False, True), repeat=2)
        }
        response = get_featured_challenges()
        assert isinstance(response, QuerySet)
        assert response.count() == 1
        assert response.first() == challenges[(True, False)]

    def test_get_authors_empty(self, db):
        response = get_authors('test@gmail.com')
        assert isinstance(response, QuerySet)
        assert response.count() == 0

    def test_get_authors(self, db, debug):
        staff_options = (False, True)
        # User e-mail cannot be null (refactor get_authors)
        email_options = ('', 'exclude@gmail.com', 'valid@gmail.com')

        authors = {
            (staff, email): mommy.make('UserProfile', user__is_staff=staff, user__email=email)
            for staff, email in product(staff_options, email_options)
        }
        response = get_authors('exclude@gmail.com')
        assert isinstance(response, QuerySet)
        assert response.count() == 1
        assert response.first() == authors[(False, 'valid@gmail.com')]
