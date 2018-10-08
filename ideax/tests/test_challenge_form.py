from django.core.files.uploadedfile import SimpleUploadedFile
from model_mommy import mommy

from ideax.forms import ChallengeForm


class TestChallengeForm:
    def test_invalid(self, snapshot):
        form = ChallengeForm({})
        assert not form.is_valid()
        assert len(form.errors) == 7
        snapshot.assert_match(form.errors)

    def test_valid(self, db, test_image):
        category = mommy.make('Category')
        data = {
            'title': 'Documento Único',
            'description': 'Redução do número de documentos para os órgãos públicos',
            'summary': 'Redução ...',
            'limit_date': '2018-12-31',
            'requester': 'Juracy Filho',
            'category': category.id,
        }

        form = ChallengeForm(data, files={
            'image': SimpleUploadedFile('favicon.png', test_image)
        })
        assert form.errors == {}
        assert form.is_valid()
