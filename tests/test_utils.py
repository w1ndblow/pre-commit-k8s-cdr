# -*- coding: utf-8 -*-
#simport fixter
from k8s_crd.utils import check_kind_in_schemas, get_url_by_kind, check_common_kind, get_yaml_docs
from k8s_crd.fixter import SCHEMAS , common_schemas_store_pattern, common_schemas_store_url
import pytest
import yaml
import copy


# SCHEMAS = {
#     "https://raw.githubusercontent.com/fluxcd-community/flux2-schemas/refs/heads/main/all.json": [
#         "HelmRelease",
#         "GitRepository",
#         "OCIRepository",
#         "Provider"
#         ],
# }

tschemas = copy.deepcopy(SCHEMAS)

@pytest.mark.parametrize(
    'x, y', [
        ('test_flux.yaml', True),
        ('test_postgres.yaml', False)
        ])
def test_kind_in_schemas(x, y):
    with open('tests/'+x) as f:
       tdocs = yaml.safe_load(f)
    tkind = tdocs['kind']
    assert check_kind_in_schemas(tkind, tschemas ) == y


def test_get_ulr_by_kind():
    turl = get_url_by_kind('HelmRelease', tschemas)
    assert turl == "https://raw.githubusercontent.com/fluxcd-community/flux2-schemas/refs/heads/main/all.json"


def test_check_common_kind():
    with open('tests/test_postgres.yaml') as f:
       tdoc = yaml.safe_load(f)
    turl = check_common_kind('Cluster',
                            common_schemas_store_pattern,
                            common_schemas_store_url,
                            tdoc)
    assert turl == "https://raw.githubusercontent.com/datreeio/CRDs-catalog" \
                   "/main/postgresql.cnpg.io/cluster_v1.json"

@pytest.mark.parametrize(
        'x, y', [
            ('test_flux.yaml', 1),
            ('test_multiple.yaml', 3),
            ('empty.yaml', 0)
            ])
def test_number_of_docs(x, y):
    with open(f'tests/{x}') as f:
        stream = get_yaml_docs(f)
    assert len(stream) == y
