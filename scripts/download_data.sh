#!/bin/bash
# Download public, no-key data into data/raw/.
# This shell version is the path actually tested in the build sandbox,
# where direct curl succeeded while Python requests intermittently timed
# out on FRED. The Python version, scripts/download_data.py, does the
# same downloads and is kept for readers who prefer Python.
# Run from the project root: bash scripts/download_data.sh
set -e
cd "$(dirname "$0")/.."
mkdir -p data/raw
for id in NASDAQCOM DJIA SP500 VIXCLS DGS10 DGS2 FEDFUNDS CPIAUCSL; do
  lower=$(echo "$id" | tr 'A-Z' 'a-z')
  curl -sL "https://fred.stlouisfed.org/graph/fredgraph.csv?id=$id" -o "data/raw/fred_${lower}.csv"
  echo "$id -> data/raw/fred_${lower}.csv"
done
echo "Yahoo S and P 500 daily closes are downloaded by scripts/download_data.py"
echo "(Yahoo chart API, no key). In this build they were saved as data/raw/yahoo_sp500_daily.csv."
