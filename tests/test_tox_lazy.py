import nctoolkit as nc

nc.options(lazy=True)
import pandas as pd
import xarray as xr
import os, pytest


ff = "data/sst.mon.mean.nc"
ff1 = "data/woa18_decav_t01_01.nc"
ff2 = "data/woa18_decav_t02_01.nc"


class TestToxar:
    def test_xarray2(self):
        tracker = nc.open_data(ff1)
        x = tracker.to_xarray(decode_times=True).time.dt.year.values[0]
        assert x == 1986
        ds = nc.open_data("data/sst.mon.mean.nc")
        assert len(ds.to_xarray(time = range(0, 3)).time.values) == 3







