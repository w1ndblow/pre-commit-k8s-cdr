#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 23 15:02:34 2025

@author: windblow
"""

import setuptools

setuptools.setup(
    packages=setuptools.find_packages(include=['k8s_crd', 'k8s_crd.*']),)
