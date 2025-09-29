#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 22 13:17:42 2025

@author: windblow
"""

#import asyncio
import sys
from .utils import fix_file
# import os


SCHEMAS = {
    "https://raw.githubusercontent.com/fluxcd-community/flux2-schemas/refs/heads/main/all.json": [
        "HelmRelease",
        "HelmRepository",
        "GitRepository",
        "OCIRepository",
        "Provider"
        ],
}

common_schemas_store_url = 'https://raw.githubusercontent.com' \
                           '/datreeio/CRDs-catalog/main/'

common_schemas_store_pattern = '{Group}/{ResourceKind}_' \
                               '{ResourceAPIVersion}.json'

ignore_types = [
    'Kustomization'
]


errors: list = []


def main():
    results = []
    for arg in sys.argv[1:]:
        try:
            result = fix_file(
                       arg,
                       SCHEMAS,
                       common_schemas_store_pattern,
                       common_schemas_store_url,
                       ignore_types)
            if result:
                print(f'Adding mark to docs in file {arg}')
            results.append(result)
        except Exception as ex:
            _collectErrors({"source": arg, "message": f"{type(ex).__name__} {ex.args}"})

    if len(errors) > 0:
        _printErrors()
        return 1

    if 1 in results:
        return 1

    return 0


def _collectErrors(error):
    errors.append(error)


def _printErrors():
    for i in errors:
        print(f"[ERROR] {i['source']}: {i['message']}")


if __name__ == '__main__':
    raise SystemExit(main())
