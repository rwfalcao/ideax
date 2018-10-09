# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestIdeaFormUpdate.test_invalid 1'] = {
    'oportunity': [
        'Este campo é obrigatório.'
    ],
    'solution': [
        'Este campo é obrigatório.'
    ],
    'target': [
        'Este campo é obrigatório.'
    ],
    'title': [
        'Este campo é obrigatório.'
    ]
}
