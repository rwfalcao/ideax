# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestCategoryForm.test_invalid 1'] = {
    'description': [
        'Este campo é obrigatório.'
    ],
    'title': [
        'Este campo é obrigatório.'
    ]
}
