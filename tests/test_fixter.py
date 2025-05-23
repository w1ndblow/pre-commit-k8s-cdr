# -*- coding: utf-8 -*-

import pytest
import os
import shutil
import glob
from k8s_crd.utils import fix_file
from k8s_crd.fixter import SCHEMAS, common_schemas_store_pattern, common_schemas_store_url

@pytest.fixture()
def file_fixture():
    os.mkdir('tests/fixture')
    for i in glob.glob('tests/*.yaml'):
        shutil.copy(i, 'tests/fixture')
    yield
    shutil.rmtree('tests/fixture')

@pytest.mark.usefixtures('file_fixture')
def test_fixter():
    COUNTS = {
    'empty.yaml': 0,
    'test_flux.yaml': 1,
    'test_multiple.yaml': 3,
    'test_postgres.yaml': 1,
    'default_k8s.yaml': 0,
    'list.yaml': 0
    }
    for i in glob.glob('tests/fixture/*.yaml'):
        fix_file(i, SCHEMAS, common_schemas_store_pattern, common_schemas_store_url)
    for i in glob.glob('tests/fixture/*.yaml'):
        with open(i) as f:
            content = f.read()
            countmarks = content.count('yaml-language-server:')
        if os.path.basename(i) == 'test_postgres.yaml':
            assert 'CRDs-catalog'  in content
        assert countmarks == COUNTS[os.path.basename(i)]
