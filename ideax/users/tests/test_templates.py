from django.shortcuts import render


class TestUserTemplates:
    def test_profile_no_idea(self, rf, common_user):
        request = rf.get('/')
        response = render(
            request,
            'users/profile.html',
            {
                'user': common_user,
                'ideas': [],
            }
        )
        assert 'Author of 0 ideas' in response.content.decode('utf-8')

    def test_profile_one_idea(self, rf, common_user):
        request = rf.get('/')
        response = render(
            request,
            'users/profile.html',
            {
                'user': common_user,
                'ideas': [1],
            }
        )
        assert 'Author of one idea' in response.content.decode('utf-8')

    def test_profile_one_idea_ptbr(self, rf, common_user, set_pt_br_language):
        request = rf.get('/')
        response = render(
            request,
            'users/profile.html',
            {
                'user': common_user,
                'ideas': [1],
            }
        )

        assert 'Autor de uma ideia' in response.content.decode('utf-8')

    def test_profile_several_ideas(self, rf, common_user):
        request = rf.get('/')
        response = render(
            request,
            'users/profile.html',
            {
                'user': common_user,
                'ideas': [1, 2],
            }
        )
        assert 'Author of 2 ideas' in response.content.decode('utf-8')

    def test_profile_user_data(self, rf, common_user):
        request = rf.get('/')
        response = render(
            request,
            'users/profile.html',
            {
                'user': common_user,
                'ideas': [],
            }
        )

        body = response.content.decode('utf-8')
        assert 'Common Idea' in body
        assert 'common.idea@dtplabs.in' in body
        assert '<img class="gravatar"' in body

    def test_profile_user_data_noname(self, rf, common_user):
        common_user.get_full_name = lambda: ''
        common_user.username = 'common-username'
        request = rf.get('/')
        response = render(
            request,
            'users/profile.html',
            {
                'user': common_user,
                'ideas': [],
            }
        )

        body = response.content.decode('utf-8')
        assert 'common-username' in body
