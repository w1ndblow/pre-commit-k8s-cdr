#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 22 13:17:42 2025

@author: windblow
"""

#import asyncio
import sys
from k8s_crd import utils
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

common_schemas_store_url =  'https://raw.githubusercontent.com' \
                            '/datreeio/CRDs-catalog/main/'

common_schemas_store_pattern = '{Group}/{ResourceKind}_' \
                               '{ResourceAPIVersion}.json'

errors: list = []

def main():
    try:
        for arg in sys.argv[1:]:
            utils.fix_file(arg,
                       SCHEMAS,
                       common_schemas_store_url,
                       common_schemas_store_pattern)
    except Exception as ex:
        _collectErrors({"source": arg, "message": f"{type(ex).__name__} {ex.args}"})

    if len(errors) > 0:
        _printErrors()
        exit(1)

def _collectErrors(error):
    errors.append(error)

def _printErrors():
    for i in errors:
        print(f"[ERROR] {i['source']}: {i['message']}")


if __name__=='__main__':
    main()
