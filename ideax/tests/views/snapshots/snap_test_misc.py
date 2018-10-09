# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestNonMiscView.test_get_phases 1'] = [
    (
        1,
        'Discussão'
    ),
    (
        2,
        'Avaliação'
    ),
    (
        3,
        'Ideação'
    ),
    (
        4,
        'Aprovação'
    ),
    (
        5,
        'Evolução'
    ),
    (
        6,
        'Concluídas'
    ),
    (
        7,
        'Arquivadas'
    ),
    (
        8,
        'Pausadas'
    )
]
