# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestCategoryForm.test_invalid 1'] = {
    'description': [
        'This field is required.'
    ],
    'title': [
        'This field is required.'
    ]
}
