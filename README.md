# matchup_pge

Production runner for MEaSUREs WVCC sounder/imager collocation datasets. This
package orchestrates parallel execution of two collocation pipelines on
AIRS/SIPS infrastructure:

- **AIRS/MODIS 1-km Matchup Indexes** — Aqua AIRS L1B sounder matched with MODIS
  MYD03 imager geolocation
  (DOI: [10.5067/MEASURES/WVCC/DATA210](https://doi.org/10.5067/MEASURES/WVCC/DATA210))
- **SNPP CrIS/VIIRS 750-m Matchup Indexes** — SNPP CrIS L1B sounder matched with
  VIIRS VNP03MOD imager geolocation
  (DOI: [10.5067/MEASURES/WVCC/DATA211](https://doi.org/10.5067/MEASURES/WVCC/DATA211))
- **JPSS-1 CrIS/VIIRS 750-m Matchup Indexes** — JPSS-1 (NOAA-20) CrIS L1B matched
  with VIIRS VJ103MOD imager geolocation
  (DOI: [10.5067/MEASURES/WVCC/DATA212](https://doi.org/10.5067/MEASURES/WVCC/DATA212))

The collocation algorithms themselves (Wang et al. 2016) live in two companion
repositories:

- [`AIRS_MODIS_collocation-master`](https://github.com/JPL-WVCC/AIRS_MODIS_collocation-master)
- [`CrIS_VIIRS_collocation-master`](https://github.com/JPL-WVCC/CrIS_VIIRS_collocation-master)

## Repository layout

```
matchup_pge/
├── matchup/
│   ├── airs_modis_parallel_run_matchup.py  # AIRS/MODIS production runner
│   ├── parallel_run_matchup.py             # CrIS/VIIRS production runner (SNPP & J1)
│   ├── compress_nc.py                      # Post-processing: nccopy deflate
│   ├── insert_metadata.py                  # Post-processing: add CF metadata
│   └── process_invalid_coordinates.py      # Post-processing: fix invalid lat/lon
├── scripts/
│   ├── download_viirs.py                   # Download VJ103MOD/VNP03MOD from LAADS DAAC
│   └── reorganize_viirs.sh                 # Symlink wget mirror layout into expected layout
├── docker/                                 # (legacy, not used for production)
├── util/
├── run_matchup.sh                          # (legacy wrapper)
├── requirements.txt
└── README.md
```

## Environment

Production runs on AIRS/SIPS machines (`drought`, `freeze`, `typhoon`). **Do not
run production on `weather2`** — it is a gateway machine only.

### Python

- Python 3.8+
- Dependencies: `numpy`, `netCDF4`, `pyhdf`, `pykdtree`, `h5py`

See [`requirements.txt`](requirements.txt). Lei Pan's anaconda3 environment at
`~leipan/anaconda3` on AIRS/SIPS is pre-configured with all dependencies:

```bash
export PATH=/home/leipan/anaconda3/bin:$PATH
python -c "import numpy, netCDF4, pyhdf, pykdtree, h5py; print('OK')"
```

If setting up a fresh environment:

```bash
conda create -n measures-wvcc python=3.8
conda activate measures-wvcc
pip install -r requirements.txt
```

### Companion code

The two collocation library repos need to be accessible on `sys.path`. The
production runners hard-code these paths at the top:

```python
sys.path.append('/home/leipan/pge/CrIS_VIIRS_collocation-master/')
sys.path.append('/home/leipan/pge/AIRS_MODIS_collocation-master/')
```

Either keep them at those paths, or edit the runners to point at your clones.

## Input data

| Dataset         | Path on AIRS/SIPS                                   |
|-----------------|-----------------------------------------------------|
| AIRS L1B        | `/archive/AIRSOps/airs/gdaac/v5/{YYYY}/{MM}/{DD}/airibrad/` |
| MODIS MYD03     | `/peate_archive/NPPOps/aqua_modis/laads/061/{YYYY}/{MM}/{DD}/aqua_modis_myd03/` |
| SNPP CrIS L1B   | `/peate_archive/NPPOps/snpp/gdisc/2/{YYYY}/{MM}/{DD}/crisl1b/` |
| J1 CrIS L1B     | `/peate_archive/NPPOps/jpss1/gdisc/3/{YYYY}/{MM}/{DD}/crisl1b/` (v3 required) |
| SNPP VIIRS      | `/raid15/leipan/VIIRS/VNP03MOD/{YYYY}/{DOY}/` (download separately) |
| J1 VIIRS        | `~/measures/VIIRS/VJ103MOD/{YYYY}/{DOY}/` (download separately) |

VIIRS geolocation is **not** available on AIRS/SIPS by default; see
[Downloading VIIRS](#downloading-viirs-vj103mod--vnp03mod) below.

## Running production

### AIRS/MODIS

```bash
cd matchup_pge/matchup
python airs_modis_parallel_run_matchup.py \
  --y 2024 --m 1 --d1 1 --d2 31 \
  --pr /path/to/output/AIRS-MODIS/ \
  --ar /archive/AIRSOps/airs/gdaac/v5/ \
  --mr /peate_archive/NPPOps/aqua_modis/laads/061/ \
  --c 36
```

Arguments:
- `--y` year, `--m` month, `--d1`/`--d2` start/end day (inclusive)
- `--pr` output product root (year/month/day/granule subdirs are created)
- `--ar` AIRS L1B root, `--mr` MODIS MYD03 root
- `--c` CPU count (number of parallel granule processes)

The runner is idempotent — existing output granules are skipped, so it is safe
to re-run after interruption.

### SNPP CrIS/VIIRS

```bash
cd matchup_pge/matchup
python parallel_run_matchup.py \
  --y 2020 --m 1 --d1 1 --d2 31 --sp SNPP \
  --pr /path/to/output/SNPP_CrIS-VIIRS/ \
  --cr /peate_archive/NPPOps/snpp/gdisc/2/ \
  --vr /raid15/leipan/VIIRS/VNP03MOD/ \
  --c 36
```

### J1 CrIS/VIIRS

```bash
cd matchup_pge/matchup
python parallel_run_matchup.py \
  --y 2024 --m 1 --d1 1 --d2 31 --sp J1 \
  --pr /path/to/output/J1_CrIS_VIIRS/ \
  --cr /peate_archive/NPPOps/jpss1/gdisc/3/ \
  --vr /path/to/VJ103MOD/ \
  --c 36
```

**Note on CrIS v3 time format:** JPSS-1 CrIS L1B v3 files use
`time_coverage_start = "YYYY-MM-DDTHH:MM:SS.00Z"` (with fractional seconds),
while v2 uses `"YYYY-MM-DDTHH:MM:SSZ"`. `parallel_run_matchup.py` handles both.

### Backgrounding long runs

Production runs for a full month take ~3-4 hours with 36 cores. Use `nohup` to
survive SSH disconnects:

```bash
nohup bash run_2023_2025.sh > production.log 2>&1 &
```

## Downloading VIIRS (VJ103MOD / VNP03MOD)

Qing Yue confirmed that running without local VIIRS data is impractical — the
collocation code opens ~800 VIIRS files per CrIS granule (~200,000 file opens
per day of production). Remote access (OPeNDAP, S3) would be 10-50x slower than
local disk at production scale.

Use `scripts/download_viirs.py` to fetch from LAADS DAAC:

```bash
# 1. Get an Earthdata Bearer token from:
#    https://ladsweb.modaps.eosdis.nasa.gov/profile/#app-keys

# 2. Download (J1 example)
python scripts/download_viirs.py \
  --product VJ103MOD \
  --years 2023 2024 2025 \
  --token "eyJ0eXAiOiJKV1Q..." \
  --output /path/to/VJ103MOD \
  --workers 4

# 3. wget mirrors the URL path; reorganize to the layout parallel_run_matchup.py expects:
./scripts/reorganize_viirs.sh /path/to/VJ103MOD
```

`download_viirs.py` is idempotent — re-running skips already-downloaded days,
so retry after network failures.

## Output format

Each CrIS (or AIRS) granule produces a directory containing one or more
NetCDF4 index files that enumerate the matching VIIRS (or MODIS) pixels for
each sounder footprint. Global attributes include:

- `SHORT_NAME`, `TITLE`, `IDENTIFIER_PRODUCT_DOI`
- `RANGEBEGINNINGDATE`, `RANGEENDINGDATE`
- `NORTHBOUNDINGCOORDINATE`, `SOUTHBOUNDINGCOORDINATE`,
  `EASTBOUNDINGCOORDINATE`, `WESTBOUNDINGCOORDINATE`
- `PRODUCTIONDATE`, `TIME_TOLERANCE` (900s for CrIS/VIIRS)

A `manifest.mf` file in each output directory records the input granules used
for that matchup.

## References

- Wang, L., B. Chen, Q. Yue, and E. Fetzer (2016), *Combining AIRS, MODIS, and
  CALIOP observations to identify contrail and contrail-induced cirrus in the
  upper troposphere*, J. Geophys. Res. Atmos., 121, 11,547–11,568.
- MEaSUREs WVCC project page:
  https://disc.gsfc.nasa.gov/information/project?title=MEaSUREs

## Production history

- **2002-2022**: AIRS/MODIS initial production (Lei Pan)
- **2015-2021**: SNPP CrIS/VIIRS initial production (Lei Pan)
- **2018-2022**: J1 CrIS/VIIRS initial production (Lei Pan)
- **2023-2025**: AIRS/MODIS and J1 CrIS/VIIRS extension (Gerald Manipon, 2026)
  - Added VJ103MOD download tooling (`scripts/download_viirs.py`)
  - Added CrIS v3 time format support to `parallel_run_matchup.py`
