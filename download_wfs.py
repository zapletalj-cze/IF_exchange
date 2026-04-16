# ============================================================
# Author: Jakub Zapletal
# Date: 2026-04-16
# Version: 1.1
# Description: Download all WFS layers clipped to an AOI
# ============================================================

import warnings
from pathlib import Path

import geopandas as gpd
from owslib.wfs import WebFeatureService


wfs_url = "https://example.com/geoserver/wfs"
aoi_path = Path("aoi.gpkg")
outdir = Path("wfs_downloads")
wfs_version = "2.0.0"
layer_threshold = 3

outdir.mkdir(parents=True, exist_ok=True)

wfs = WebFeatureService(url=wfs_url, version=wfs_version)
layers = list(wfs.contents.keys())
n_layers = len(layers)

if n_layers > layer_threshold:
    warnings.warn(
        f"WFS exposes {n_layers} layers (threshold {layer_threshold}). "
        f"Starting download to {outdir}",
        stacklevel=2,
    )

first_layer = wfs.contents[layers[0]]
target_crs = first_layer.crsOptions[0].getcode() if first_layer.crsOptions else "EPSG:4326"

aoi = gpd.read_file(aoi_path).to_crs(target_crs)
bbox = tuple(aoi.total_bounds)

saved_files = []

for layer_name in layers:
    try:
        try:
            response = wfs.getfeature(
                typename=layer_name,
                bbox=(*bbox, target_crs),
                outputFormat="application/json",
            )
            gdf = gpd.read_file(response)
        except Exception:
            response = wfs.getfeature(
                typename=layer_name,
                bbox=(*bbox, target_crs),
                outputFormat="GML3",
            )
            gml_path = outdir / f"_tmp_{layer_name.replace(':', '_')}.gml"
            with open(gml_path, "wb") as f:
                f.write(response.read())
            gdf = gpd.read_file(gml_path)
            gml_path.unlink(missing_ok=True)

        if gdf.empty:
            continue

        safe_name = layer_name.replace(":", "_").replace("/", "_")
        out_path = outdir / f"{safe_name}.gpkg"
        gdf.to_file(out_path, driver="GPKG", layer=safe_name)
        saved_files.append(out_path)

    except Exception as e:
        warnings.warn(f"Failed to download {layer_name}: {e}", stacklevel=2)

print(f"Downloaded {len(saved_files)} layers")
