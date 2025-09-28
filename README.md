# Kubernetes manifest precommit hooks

This repository contain [pre-commit hooks](https://pre-commit.com/) , witch helps for work with k8s manifests, for example, with Gitops flux approach

## fix-mark-k8s-crd-yaml

This hook automatically fix files for add mark of [yaml server language](https://github.com/redhat-developer/yaml-language-server) in start of yaml document for well known custom kinds crd witch get in copyleft [catalog](https://github.com/datreeio/CRDs-catalog) . It usefull for IDE like vim and Visual Studio Code.

To use this hook add config below in `.pre-commit-config.yaml`  of your code project

```
repos:
  - repo: https://github.com/w1ndblow/pre-commit-k8s-cdr
    rev: 0.0.3
    hooks:
      - id: fix-mark-k8s-crd-yaml
```

