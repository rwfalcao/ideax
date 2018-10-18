from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import PermissionDenied
from django.http.response import Http404

from model_mommy import mommy
from pytest import mark, raises

from ...forms import UseTermForm
from ...views import accept_use_term, save_use_term, use_term_edit


class TestAcceptUseTermView:
    def test_accept_use_term_anonymous(self, rf):
        request = rf.get('/term/accept')
        request.user = AnonymousUser()
        response = accept_use_term(request)
        assert (response.status_code, response.url) == (302, '/accounts/login/?next=/term/accept')

    def test_accept_use_term_not_accepted(self, ideax_views, rf, admin_user, messages, get_ip, mocker):
        ideax_views.audit = mocker.Mock()
        admin_user.userprofile.use_term_accept = False
        request = rf.get('/term/accept')
        request.user = admin_user
        request._messages = messages
        response = accept_use_term(request)
        assert (response.status_code, response.url) == (302, '/')
        assert messages.messages == ['Term of use accepted!']
        get_ip.assert_called_once_with(request)

    def test_accept_use_term_accepted(self, ideax_views, rf, admin_user, messages, mocker):
        ideax_views.audit = mocker.Mock()
        admin_user.userprofile.use_term_accept = True
        request = rf.get('/term/accept')
        request.user = admin_user
        request._messages = messages
        response = accept_use_term(request)
        assert (response.status_code, response.url) == (302, '/')
        assert messages.messages == ['Term of use already accepted!']


class TestUseTermEdit:
    def test_anonymous(self, rf):
        request = rf.get(f'/useterm/99999/edit/')
        request.user = AnonymousUser()
        response = use_term_edit(request, 99999)
        assert (response.status_code, response.url) == (302, '/accounts/login/?next=/useterm/99999/edit/')

    def test_not_found(self, rf, admin_user):
        request = rf.get(f'/useterm/99999/edit/')
        request.user = admin_user
        with raises(Http404):
            use_term_edit(request, 99999)

    def test_get_common_user(self, rf, common_user, ideax_views, mocker):
        request = rf.get('/useterm/1/edit/')
        request.user = common_user
        with raises(PermissionDenied):
            use_term_edit(request, 1)

    def test_get(self, rf, admin_user, ideax_views, mocker):
        use_term = mommy.make('Use_Term')
        use_term_form = mocker.patch.object(ideax_views, 'UseTermForm')
        save_use_term = mocker.patch.object(ideax_views, 'save_use_term')

        request = rf.get(f'/useterm/{use_term.id}/edit/')
        request.user = admin_user
        use_term_edit(request, use_term.id)
        use_term_form.assert_called_once_with(instance=use_term)
        save_use_term.assert_called_once_with(request, use_term_form.return_value, 'ideax/use_term_edit.html')

    def test_post(self, rf, admin_user, ideax_views, mocker):
        use_term = mommy.make('Use_Term')
        use_term_form = mocker.patch.object(ideax_views, 'UseTermForm')
        save_use_term = mocker.patch.object(ideax_views, 'save_use_term')

        request = rf.post(f'/useterm/{use_term.id}/edit/')
        request.user = admin_user
        use_term_edit(request, use_term.id)
        use_term_form.assert_called_once_with(request.POST, instance=use_term)
        save_use_term.assert_called_once_with(request, use_term_form.return_value, 'ideax/use_term_edit.html')


class TestSaveUseTerm:
    def test_get_full(self, rf, admin_user):
        # TODO: Change to a integrate test
        use_term = mommy.make('Use_Term')
        request = rf.get(f'/useterm/{use_term.id}/edit/')
        request.user = admin_user
        response = save_use_term(request, UseTermForm(instance=use_term), 'ideax/use_term_edit.html')
        body = response.content.decode('utf-8')
        assert response.status_code == 200
        assert '<form method="post" class="js-use_term-update-form"' in body
        assert "input type='hidden' name='csrfmiddlewaretoken'" in body
        assert '<button type="submit" class="btn btn-primary">Update</button>' in body

    def test_get_mocked(self, rf, admin_user, ideax_views, mocker):
        render = mocker.patch.object(ideax_views, 'render')
        request = rf.get('/')
        request.user = admin_user
        save_use_term(request, 'form', 'use_term_edit.html')
        render.assert_called_once_with(request, 'use_term_edit.html', {'form': 'form'})

    def test_post_1(self, rf, admin_user, mocker, messages):
        form = mocker.patch('ideax.ideax.forms.UseTermForm')
        form.is_valid.return_value = True
        form.save.return_value.is_invalid_date.return_value = True
        terms = mocker.patch('ideax.ideax.models.Use_Term.objects')
        terms.all.return_value = []
        render = mocker.patch('ideax.ideax.views.render')
        request = rf.post('/', {})
        request.user = admin_user
        request._messages = messages
        save_use_term(request, form, 'use_term_edit.html')
        render.assert_called_once_with(request, 'use_term_edit.html', {'form': form})
        assert messages.messages == ['Invalid Final Date']

    def test_post_new(self, rf, admin_user, mocker, messages):
        form = mocker.patch('ideax.ideax.forms.UseTermForm')
        form.is_valid.return_value = True
        form.save.return_value.is_invalid_date.return_value = False
        use_term = mocker.Mock()
        use_term.is_past_due = True
        terms = mocker.patch('ideax.ideax.models.Use_Term.objects')
        terms.all.return_value = [use_term]
        render = mocker.patch('ideax.ideax.views.render')
        request = rf.post('/', {})
        request.user = admin_user
        request._messages = messages
        save_use_term(request, form, 'use_term_edit.html', True)
        render.assert_called_once_with(request, 'use_term_edit.html', {'form': form})
        assert messages.messages == ['Already exists a active Term Of Use']

    def test_post_new_inactive(self, rf, admin_user, mocker, messages):
        form = mocker.patch('ideax.ideax.forms.UseTermForm')
        form.is_valid.return_value = True
        form.save.return_value.is_invalid_date.return_value = False
        use_term = mocker.Mock()
        use_term.is_past_due = False
        terms = mocker.patch('ideax.ideax.models.Use_Term.objects')
        terms.all.return_value = [use_term]
        request = rf.post('/', {})
        request.user = admin_user
        request._messages = messages
        response = save_use_term(request, form, 'use_term_edit.html', True)
        assert (response.status_code, response.url) == (302, '/useterm/list/')
        assert messages.messages == ['Term of Use saved successfully!']

    @mark.skip('TODO: save use term with invalid form')
    def test_post_form_invalid(self, rf, admin_user, mocker):
        form = mocker.patch('ideax.ideax.forms.UseTermForm')
        form.is_valid.return_value = False
        form.save.return_value.is_invalid_date.return_value = False
        request = rf.post('/', {})
        request.user = admin_user
        response = save_use_term(request, form, 'use_term_edit.html', True)
        # TODO: maybe a message
        assert response is not None
