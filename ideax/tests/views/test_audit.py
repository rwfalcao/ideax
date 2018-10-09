from ...views import audit


class MockLogger:
    logs = []

    def info(self, *args):
        self.logs.append(args)


class TestAudit:
    def test_audit(self, ideax_views):
        logger = MockLogger()
        ideax_views.logger = logger
        audit('test_user', '127.0.0.1', 'TEST', 'TestAudit', 444)
        assert len(logger.logs) == 1
        assert logger.logs[0] == (
            '%(username)s|%(ip_addr)s|%(operation)s|%(className)s|%(objectId)s',
            {
                'username': 'test_user',
                'ip_addr': '127.0.0.1',
                'operation': 'TEST',
                'className': 'TestAudit',
                'objectId': 444,
            }
        )
