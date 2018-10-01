class TestViews(object):
    def test_frontpage(self, client):
        response = client.get('/')
        body = response.content.decode('utf-8', 'strict')
        assert 'você tem um canal aberto para a inovação' in body
