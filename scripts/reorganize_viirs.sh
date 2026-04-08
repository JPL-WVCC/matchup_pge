#!/bin/bash
#
# Reorganize VIIRS data after wget download.
#
# wget -m mirrors the full URL path, so VJ103MOD/VNP03MOD files land at:
#   {root}/{year}/{product}/{year}/{doy}/VJ103MOD.*.nc
#
# parallel_run_matchup.py expects:
#   {root}/{year}/{doy}/VJ103MOD.*.nc
#
# This script creates symlinks to bridge the two layouts without duplicating data.
#
# Usage:
#   ./reorganize_viirs.sh /path/to/VJ103MOD [year1 year2 ...]
#   ./reorganize_viirs.sh /path/to/VNP03MOD 2022 2023 2024 2025
#

set -euo pipefail

if [ $# -lt 1 ]; then
  echo "Usage: $0 <viirs_root> [year1 year2 ...]" >&2
  exit 1
fi

ROOT="$1"
shift

if [ ! -d "$ROOT" ]; then
  echo "ERROR: $ROOT is not a directory" >&2
  exit 1
fi

# Infer product name from the path (last component) for the nested structure
PRODUCT=$(basename "$ROOT")

# If no years specified, use all year directories present
if [ $# -eq 0 ]; then
  YEARS=$(ls "$ROOT" 2>/dev/null | grep -E '^[0-9]{4}$' | sort -u)
else
  YEARS="$@"
fi

for YEAR in $YEARS; do
  SRC="$ROOT/$YEAR/$PRODUCT/$YEAR"
  if [ ! -d "$SRC" ]; then
    echo "  $YEAR: skip (no mirrored data at $SRC)"
    continue
  fi

  count=0
  for doy_dir in "$SRC"/*/; do
    doy=$(basename "$doy_dir")
    target="$ROOT/$YEAR/$doy"
    if [ ! -e "$target" ]; then
      ln -s "$SRC/$doy" "$target"
      count=$((count + 1))
    fi
  done
  echo "  $YEAR: $count day symlinks created"
done

echo "Done. VIIRS data ready for parallel_run_matchup.py"
