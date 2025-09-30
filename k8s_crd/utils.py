# -*- coding: utf-8 -*-


import yaml
import requests


def fix_file(fd: str,
             schemas: dict,
             pattern: str,
             url_shema: str,
             ignore_types: list):
    file_lines = []
    urls = []
    with open(fd) as f:
        file_lines = f.readlines()
    with open(fd) as f:
        yamldocs = get_yaml_docs(f)
        for doc in yamldocs:
            if isinstance(doc, dict) and doc.get('kind', None):
                kind = doc['kind']
                if kind in ignore_types:
                    continue
                if check_kind_in_schemas(kind, schemas):
                    url = get_url_by_kind(kind, schemas)
                    urls.append(url)
                # it may common type
                else:
                    if (url:=check_common_kind(kind, pattern, url_shema, doc)):
                       #  set_schema_url(url):
                      schemas[url] = [ kind ]
                      urls.append(url)
    result = 0
    if not urls:
        return result
    for i,s in enumerate(file_lines):
        if s == "---\n":
            if '# yaml-language-server: ' not in file_lines[i+1]:
                file_lines.insert(
                    i+1,
                    '# yaml-language-server: $schema={}\n'.format(
                        urls.pop(0)))
                result = 1
            else:
                urls.pop(0)
        elif i == 0 and not s == "---\n" and \
            not s.startswith('# yaml-language-server'):
            file_lines.insert(i,
                '# yaml-language-server: $schema={}\n'.format(
                    urls.pop(0)))
            result = 1
        if not urls:
            break
    with open(fd, 'w') as f:
        f.writelines(file_lines)
    return result


def check_kind_in_schemas(kind: str, schemas: dict) -> bool:
    kinds_on_schemas = []
    for i in schemas.values():
        kinds_on_schemas.extend(i)
    if kind in kinds_on_schemas:
        return True
    else:
        return False


def get_url_by_kind(kind: str, schemas: dict) -> str:
    for k in schemas.keys():
        for v in schemas.values():
            if kind in v:
                return k
    return ''

# @functools.lru_cache()
def check_common_kind(kind: str, pattern: str, url: str, doc: dict) -> str:
    if '/' in doc['apiVersion']:
        group, api_ver = doc['apiVersion'].split('/')
    else:
        group, api_ver = '', doc['apiVersion']
    url_shema = url + pattern.format(
        Group=group,
        ResourceKind=kind.lower(),
        ResourceAPIVersion=api_ver,
        )
    if requests.get(url_shema).status_code == 200:
        return url_shema


def get_yaml_docs(file):
    yamldocs = yaml.load_all(file, yaml.FullLoader)
    return [ *yamldocs ]
