#!/usr/bin/env bash

mvn clean compile package

podman build --arch amd64 --os linux -t quay.io/novacrest/novacrest-customer-api:1.0.0 -f deployment/Dockerfile .
podman push quay.io/novacrest/novacrest-customer-api:1.0.0
