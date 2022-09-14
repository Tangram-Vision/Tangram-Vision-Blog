#!/usr/bin/env bash

set -euo pipefail

THIS_DIR=$(dirname $0)

function on_rust_latest() {
    local current_manifest=$(cat rust-latest.digest)
    local latest_manifest=$("${THIS_DIR}/latest-rust-manifest-digest.sh")

    [[ ${current_manifest} = ${latest_manifest} ]]
}

function bump_image_version() {
    local version_file="${THIS_DIR}/VERSION"
    local new_version=$(mawk -F. '{ $NF=$NF+1; print }' OFS=. ${version_file})

    tee <<<"${new_version}" ${version_file}
}

function check() {
    if on_rust_latest; then
        echo "Already on Rust latest; nothing to do."
    else
        "${THIS_DIR}/latest-rust-manifest-digest.sh" > "${THIS_DIR}/rust-latest.digest"

        local version=$(bump_image_version)

        git config user.email "gitlab-bots@example.com"

        REPO_PATH=$(git remote get-url origin | sed -E 's/^.*gitlab\.com.//')

        git remote set-url origin "<https://CI-Bot:${PROJECT_ACCESS_TOKEN}@gitlab.com/${REPO_PATH}>"

        git switch "${CI_COMMIT_REF_NAME}"
        git add --update
        git commit -m "Apply patch bump (v${version}) because of new Rust:latest image"

        git push
    fi
}

check
