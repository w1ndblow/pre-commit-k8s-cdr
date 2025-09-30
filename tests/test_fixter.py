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


@pytest.mark.parametrize('yaml_file, count', [
    ('empty.yaml', 0),
    ('test_flux.yaml', 1),
    ('test_multiple.yaml', 3),
    ('test_postgres.yaml', 1),
    ('default_k8s.yaml', 0),
    ('list.yaml', 0),
    ('test_without_start_token.yaml', 1),
    ('external_secret.yaml', 1),
    ('test_exist.yaml', 1),
    ('test_with_base_and_custom.yaml', 1),
    ('test_with_custom_and_base.yaml', 1),
])
@pytest.mark.usefixtures('file_fixture')
def test_fixter(yaml_file, count):
    fix_file(f'tests/fixture/{yaml_file}',
                SCHEMAS,
                common_schemas_store_pattern,
                common_schemas_store_url,
                [])
    with open(f'tests/fixture/{yaml_file}') as f:
        content = f.read()
        countmarks = content.count('yaml-language-server:')
    if yaml_file == 'test_postgres.yaml':
        assert 'CRDs-catalog' in content
    if yaml_file == 'external_secret.yaml':
        assert 'externalsecret_v1beta1' in content
    assert countmarks == count
