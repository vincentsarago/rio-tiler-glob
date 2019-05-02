"""rio_tiler_glob: tiler."""

import re
import os
import multiprocessing
from functools import partial
from concurrent import futures

import numpy as np
import numexpr as ne

import mercantile

from rio_tiler import utils

# ref: https://docs.python.org/3/library/concurrent.futures.html#threadpoolexecutor
MAX_THREADS = int(os.environ.get("MAX_THREADS", multiprocessing.cpu_count() * 5))


def metadata(addresses, pmin=2, pmax=98, **kwargs):
    """
    Return image bounds and band statistics.

    Attributes
    ----------
    addresses : str or PathLike object
        A dataset path or URL. Will be opened in "r" mode.
    pmin : int, optional, (default: 2)
        Histogram minimum cut.
    pmax : int, optional, (default: 98)
        Histogram maximum cut.
    kwargs : optional
        These are passed to 'rio_tiler.utils.raster_get_stats'
        e.g: overview_level=2, dst_crs='epsg:4326'

    Returns
    -------
    out : dict
        Dictionary with image bounds and bands statistics.

    """
    _stats_worker = partial(
        utils.raster_get_stats, indexes=[1], percentiles=(pmin, pmax), **kwargs
    )
    with futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        info = list(executor.map(_stats_worker, addresses))

    meta = {
        "bounds": info[0]["bounds"],
        "minzoom": info[0]["minzoom"],
        "maxzoom": info[0]["minzoom"],
    }
    band_descriptions = [
        [ix + 1, os.path.basename(d)] for ix, d in enumerate(addresses)
    ]
    meta["band_descriptions"] = band_descriptions
    meta["statistics"] = {
        band_descriptions[ix][0]: r["statistics"][1] for ix, r in enumerate(info)
    }
    return meta


def tile(addresses, tile_x, tile_y, tile_z, tilesize=256, **kwargs):
    """
    Create mercator tile from any images.

    Attributes
    ----------
    addresses : str
        file url.
    tile_x : int
        Mercator tile X index.
    tile_y : int
        Mercator tile Y index.
    tile_z : int
        Mercator tile ZOOM level.
    tilesize : int, optional (default: 256)
        Output image size.
    kwargs: dict, optional
        These will be passed to the 'rio_tiler.utils.tile_read' function.

    Returns
    -------
    data : numpy ndarray
    mask: numpy array

    """
    mercator_tile = mercantile.Tile(x=tile_x, y=tile_y, z=tile_z)
    tile_bounds = mercantile.xy_bounds(mercator_tile)

    _tiler = partial(utils.tile_read, bounds=tile_bounds, tilesize=tilesize, **kwargs)
    with futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        data, masks = zip(*list(executor.map(_tiler, addresses)))
        mask = np.all(masks, axis=0).astype(np.uint8) * 255

    return np.concatenate(data), mask


def expression(addresses, tile_x, tile_y, tile_z, expr=None, **kwargs):
    """
    Apply expression on data.

    Attributes
    ----------
    sceneid : str
        Landsat id, Sentinel id, CBERS ids or file url.

    tile_x : int
        Mercator tile X index.
    tile_y : int
        Mercator tile Y index.
    tile_z : int
        Mercator tile ZOOM level.
    expr : str, required
        Expression to apply (e.g '(B5+B4)/(B5-B4)')
        Band name should start with 'B'.

    Returns
    -------
    out : ndarray
        Returns processed pixel value.

    """
    if not expr:
        raise Exception("Missing expression")

    bands_names = tuple(set(re.findall(r"b(?P<bands>[0-9A]{1,2})", expr)))
    arr, mask = tile(addresses, tile_x, tile_y, tile_z, **kwargs)

    ctx = {}
    for bdx, b in enumerate(bands_names):
        ctx["b{}".format(b)] = arr[bdx]

    rgb = expr.split(",")
    return (
        np.array(
            [np.nan_to_num(ne.evaluate(bloc.strip(), local_dict=ctx)) for bloc in rgb]
        ),
        mask,
    )
