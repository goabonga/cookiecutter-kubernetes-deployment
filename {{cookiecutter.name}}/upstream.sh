#!/bin/bash

NAME={{cookiecutter.name}}
NAMESPACE={{cookiecutter.namespace}}

helm dependency update upstream

helm template \
    --include-crds \
    --skip-tests \
    --namespace $NAMESPACE  \
    $NAME \
    -f upstream/values.yaml \
    ./upstream > resources/upstream.yaml
