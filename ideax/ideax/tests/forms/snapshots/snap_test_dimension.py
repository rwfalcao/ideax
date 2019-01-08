# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestDimensionForm.test_max_ptbr 1'] = {
    'description': [
        'Certifique-se de que o valor tenha no máximo 500 caracteres (ele possui 501).'
    ],
    'title': [
        'Certifique-se de que o valor tenha no máximo 200 caracteres (ele possui 201).'
    ]
}

snapshots['TestDimensionForm.test_invalid 1'] = {
    'description': [
        'Este campo é obrigatório.'
    ],
    'init_date': [
        'Este campo é obrigatório.'
    ],
    'title': [
        'Este campo é obrigatório.'
    ],
    'weight': [
        'Este campo é obrigatório.'
    ]
}

snapshots['TestDimensionForm.test_max 1'] = {
    'description': [
        'Certifique-se de que o valor tenha no máximo 500 caracteres (ele possui 501).'
    ],
    'title': [
        'Certifique-se de que o valor tenha no máximo 200 caracteres (ele possui 201).'
    ]
}
