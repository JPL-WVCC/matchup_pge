#!/usr/bin/env python3
"""
Download VIIRS geolocation data from LAADS DAAC for MEaSUREs WVCC production.

Supports:
  - VNP03MOD (SNPP VIIRS 750m geolocation): collection 5110
  - VJ103MOD (J1/JPSS-1 VIIRS 750m geolocation): collection 5201

Usage:
  # SNPP VIIRS
  python download_viirs.py --product VNP03MOD --years 2022 2023 2024 2025 \\
    --token YOUR_EARTHDATA_TOKEN --output /path/to/VNP03MOD --workers 4

  # J1 VIIRS
  python download_viirs.py --product VJ103MOD --years 2023 2024 2025 \\
    --token YOUR_EARTHDATA_TOKEN --output /path/to/VJ103MOD --workers 4

Get your Earthdata Bearer token from:
  https://ladsweb.modaps.eosdis.nasa.gov/profile/#app-keys

Notes:
  - wget mirrors the full URL path, so files land at:
      {output}/{year}/VJ103MOD/{year}/{doy}/VJ103MOD.*.nc
    Use the reorganize_viirs.sh script to create {output}/{year}/{doy}/ symlinks
    that match what parallel_run_matchup.py expects.
  - Re-running the script skips already-downloaded days (checks for non-empty
    directories), so it's safe to retry after failures.
"""

import argparse
import calendar
import os
import subprocess
from datetime import date
from multiprocessing import Pool


# LAADS DAAC collection IDs
COLLECTION_IDS = {
    "VNP03MOD": "5110",   # SNPP VIIRS 750m geolocation
    "VJ103MOD": "5201",   # J1/JPSS-1 VIIRS 750m geolocation
}

LAADS_BASE_URL = "https://ladsweb.modaps.eosdis.nasa.gov/archive/allData"


def download_one_day(args):
    """Download all granules for a single day."""
    product, collection_id, year, day_str, token, output_dir = args

    # Skip if the target day directory already has files (from the wget mirror layout)
    mirrored_day = os.path.join(output_dir, str(year), product, str(year), day_str)
    if os.path.exists(mirrored_day) and len(os.listdir(mirrored_day)) > 0:
        print(f"  {product} {year}/{day_str}: SKIP (already downloaded)", flush=True)
        return 0

    url = f"{LAADS_BASE_URL}/{collection_id}/{product}/{year}/{day_str}/"
    work_dir = os.path.join(output_dir, str(year))
    os.makedirs(work_dir, exist_ok=True)

    cmd = (
        f'wget -q -e robots=off -m -np -R .html,.tmp -nH --cut-dirs=3 '
        f'"{url}" '
        f'--header "Authorization: Bearer {token}" '
        f'-P {work_dir}'
    )

    p = subprocess.Popen(
        cmd, shell=True, cwd=work_dir,
        stderr=subprocess.PIPE, stdout=subprocess.PIPE,
    )
    out, err = p.communicate()
    status = "OK" if p.returncode == 0 else f"FAIL({p.returncode})"
    print(f"  {product} {year}/{day_str}: {status}", flush=True)
    return p.returncode


def main():
    parser = argparse.ArgumentParser(
        description="Download VIIRS geolocation from LAADS DAAC",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--product", required=True, choices=list(COLLECTION_IDS.keys()),
        help="VIIRS product to download",
    )
    parser.add_argument(
        "--years", required=True, nargs="+", type=int,
        help="Years to download (e.g., 2022 2023 2024 2025)",
    )
    parser.add_argument(
        "--token", required=True,
        help="Earthdata Bearer token (get from LAADS profile)",
    )
    parser.add_argument(
        "--output", required=True,
        help="Output root directory (e.g., /path/to/VJ103MOD)",
    )
    parser.add_argument(
        "--workers", type=int, default=4,
        help="Number of parallel download workers (default: 4)",
    )
    parser.add_argument(
        "--start-day", type=int, default=1,
        help="Start day-of-year (default: 1)",
    )
    parser.add_argument(
        "--end-day", type=int, default=None,
        help="End day-of-year (default: last day of year)",
    )

    args = parser.parse_args()

    product = args.product
    collection_id = COLLECTION_IDS[product]

    print(f"Product: {product}")
    print(f"Collection: {collection_id}")
    print(f"Years: {args.years}")
    print(f"Output: {args.output}")
    print(f"Workers: {args.workers}")
    print()

    os.makedirs(args.output, exist_ok=True)

    download_args = []
    for year in args.years:
        days_in_year = 366 if calendar.isleap(year) else 365
        end_day = args.end_day if args.end_day else days_in_year
        # For current year, don't go beyond today
        if year == date.today().year:
            today_doy = date.today().timetuple().tm_yday
            end_day = min(end_day, today_doy)

        for day in range(args.start_day, end_day + 1):
            day_str = str(day).zfill(3)
            download_args.append(
                (product, collection_id, year, day_str, args.token, args.output)
            )

    print(f"Total days to download: {len(download_args)}")
    print()

    with Pool(args.workers) as pool:
        results = pool.map(download_one_day, download_args)

    failed = sum(1 for r in results if r != 0)
    print(f"\nDone. {len(results) - failed}/{len(results)} days succeeded.")
    if failed:
        print(f"WARNING: {failed} days had errors. Re-run to retry.")


if __name__ == "__main__":
    main()
