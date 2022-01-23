#!/usr/bin/env bash

set -e

for tname in tests/*.py; do
  echo "[Running $tname]"
  python3.10 "$tname"
  echo ""
  echo ""
done
