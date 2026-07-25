#!/usr/bin/env bash
set -euo pipefail

destination="${1:-third_party_sources}"
mkdir -p "$destination"

download_and_verify() {
  local filename="$1"
  local url="$2"
  local expected_sha256="$3"
  local output="$destination/$filename"

  curl --fail --location --proto '=https' --tlsv1.2 "$url" --output "$output"

  if command -v sha256sum >/dev/null 2>&1; then
    printf '%s  %s\n' "$expected_sha256" "$output" | sha256sum --check -
  else
    local actual_sha256
    actual_sha256="$(shasum -a 256 "$output" | awk '{print $1}')"
    if [[ "$actual_sha256" != "$expected_sha256" ]]; then
      printf 'SHA-256 mismatch for %s\n' "$output" >&2
      exit 1
    fi
    printf '%s: OK\n' "$output"
  fi
}

download_and_verify \
  "kerykeion-5.12.9.tar.gz" \
  "https://files.pythonhosted.org/packages/d8/8f/d91e01365843509e55c81febb4fe20e4480dc2485da4311f1efc80789b6d/kerykeion-5.12.9.tar.gz" \
  "a7ef7bd6a46973913953fe0aa78cb714bd54fda4b20f01355b913fcf348f0216"

download_and_verify \
  "pyswisseph-2.10.3.2.tar.gz" \
  "https://files.pythonhosted.org/packages/66/a6/db70d67a00dda42ebd033538c086879328f4c17f670eafe8aca2f11abfef/pyswisseph-2.10.3.2.tar.gz" \
  "c54c305e83dbd5d2b71e58d8a69d8ee41de24c4d3328ce09e2af860a3537624d"
