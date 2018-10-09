# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestUseTermForm.test_invalid 1'] = {
    'final_date': [
        'Este campo é obrigatório.'
    ],
    'init_date': [
        'Este campo é obrigatório.'
    ],
    'term': [
        'Este campo é obrigatório.'
    ]
}
