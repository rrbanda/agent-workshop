#!/usr/bin/env bash

mvn clean compile package

podman build --arch amd64 --os linux -t quay.io/acme/acme-finance-api:1.0.0 -f deployment/Dockerfile .
podman push quay.io/acme/acme-finance-api:1.0.0
