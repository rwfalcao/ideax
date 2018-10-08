# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestCriterionForm.test_invalid 1'] = {
    'description': [
        'Este campo é obrigatório.'
    ],
    'peso': [
        'Este campo é obrigatório.'
    ]
}
