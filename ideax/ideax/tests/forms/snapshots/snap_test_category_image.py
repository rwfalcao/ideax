# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestCategoryImageForm.test_invalid 1'] = {
    'category': [
        'Este campo é obrigatório.'
    ],
    'description': [
        'Este campo é obrigatório.'
    ],
    'image': [
        'Este campo é obrigatório.'
    ]
}
