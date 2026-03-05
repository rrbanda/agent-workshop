#!/usr/bin/env bash

podman run -d \
  --name novacrest-finance-api \
  -p 8082:8082 \
  -e SPRING_DATASOURCE_URL=jdbc:postgresql://host.docker.internal:5432/novacrest_finance \
  -e SPRING_DATASOURCE_USERNAME=postgres \
  -e SPRING_DATASOURCE_PASSWORD=postgres \
  quay.io/novacrest/novacrest-finance-api:1.0.0
