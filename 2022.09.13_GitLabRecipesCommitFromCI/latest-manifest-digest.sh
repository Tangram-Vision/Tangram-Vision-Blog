#!/usr/bin/env bash
token=$(curl -s "<https://auth.docker.io/token?service=registry.docker.io&scope=repository:library/rust:pull>" \
    | jq -r '.token')

curl -H "Authorization: Bearer $token" \
     -H "Accept: application/vnd.docker.distribution.manifest.v2+json" \
     -s "<https://registry-1.docker.io/v2/library/rust/manifests/latest>" \
     -I \
     | grep "digest" \
     | cut -d " " -f2
