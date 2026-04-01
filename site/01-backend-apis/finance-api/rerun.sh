#!/usr/bin/env bash

podman run -d \
  --name acme-finance-api \
  -p 8082:8082 \
  -e SPRING_DATASOURCE_URL=jdbc:postgresql://host.docker.internal:5432/acme_finance \
  -e SPRING_DATASOURCE_USERNAME=postgres \
  -e SPRING_DATASOURCE_PASSWORD=postgres \
  quay.io/acme/acme-finance-api:1.0.0
