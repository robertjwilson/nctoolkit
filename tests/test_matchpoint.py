import nctoolkit as nc
import numpy as np
import pandas as pd
import xarray as xr
import os, pytest

nc.options(lazy=True)


ff = "data/sst.mon.mean.nc"
ff1 = "data/woa18_decav_t01_01.nc"



class TestCrop:
    def test_matchpoint(self):

        print("test 1")
        depths = nc.open_data("data/matchpoint_depths.nc")

        ensemble = nc.create_ensemble("data/matchpoint")[0:3]

        ds = nc.open_data("data/matchpoint/amm7_1d_20000101_20000131_ptrc_T.nc")
        levels = ds.levels
        levels += levels
        ds.subset(time = [0])
        depths = nc.open_data("data/matchpoint_depths.nc")
        # ds.subset(time = 0)
        ds.append(depths)
        ds.merge()
        ds.regrid(pd.DataFrame({"lon":[1, 2], "lat":[54.5, 54.7]}), method = "bil")


        df = ds.to_dataframe().reset_index()
        df["month" ] =  [x.month for x in df.time_counter]
        df["year"] = [x.year for x in df.time_counter]
        df["day"] = [x.day for x in df.time_counter]
        df = df.loc[:,["lon", "lat", "month", "day", "year", "N3_n", "depth"]].drop_duplicates()
        ds = nc.open_data("data/matchpoint/amm7_1d_20000101_20000131_ptrc_T.nc")
        ds.subset(time = [0])
        ds.run()

        matcher = nc.open_matchpoint()
        depths = ds.levels
        df["depth"]  = levels
        matcher.add_points(df.drop(columns = "N3_n"))
        matcher.add_data(ds, variables = "N3_n", depths = depths)
        matcher.matchup()


        assert matcher.values.rename(columns = {"N3_n":"nitrate"}).merge( df).assign(bias = lambda x: np.abs(x.N3_n - x.nitrate)).bias.max() < 0.0001
        assert len(matcher.values) == len(df)


        print("test 2")
        matcher = nc.open_matchpoint()
        depths = ds.levels
        df["depth"]  = levels
        matcher.add_points(df.drop(columns = "N3_n"))
        matcher.add_data(ds, variables = "N3_n", depths = depths)
        with pytest.raises(ValueError):
            matcher.add_data(ds, variables = "N3_n")



        matcher = nc.open_matchpoint()
        depths = ds.levels
        df["depth"]  = levels
        matcher.add_points(df.drop(columns = "N3_n"))
        matcher.add_data(ds, variables = "N3_n", depths = depths)

        depths = nc.open_data("data/matchpoint_depths.nc")

        ensemble = nc.create_ensemble("data/matchpoint")[0:3]

        ds = nc.open_data("data/matchpoint/amm7_1d_20000101_20000131_ptrc_T.nc")
        levels = ds.levels
        levels += levels
        ds.subset(time = [0])
        depths = nc.open_data("data/matchpoint_depths.nc")
        # ds.subset(time = 0)
        ds.append(depths)
        ds.merge()
        ds.regrid(pd.DataFrame({"lon":[1, 2], "lat":[54.5, 54.7]}), method = "bil")


        df = ds.to_dataframe().reset_index()
        df["month" ] =  [x.month for x in df.time_counter]
        df["year"] = [x.year for x in df.time_counter]
        df["day"] = [x.day for x in df.time_counter]
        df = df.loc[:,["lon", "lat", "month", "day", "year", "N3_n", "depth"]].drop_duplicates()
        ds = nc.open_data("data/matchpoint/amm7_1d_20000101_20000131_ptrc_T.nc")
        ds.subset(time = [0])
        ds.run()
        matcher = nc.open_matchpoint()
        depths = ds.levels
        matcher.add_data(ds, variables = "N3_n", depths = depths)

        with pytest.raises(ValueError):
            matcher.add_data(ds, variables = "N3_n")
        df["depth"]  = levels
        matcher.add_points(df.drop(columns = "N3_n"))
        matcher.matchup()


        assert matcher.values.rename(columns = {"N3_n":"nitrate"}).merge( df).assign(bias = lambda x: np.abs(x.N3_n - x.nitrate)).bias.max() < 0.0001
        assert len(matcher.values) == len(df)



        print("test 3")

        ds = nc.open_data(ensemble)
        ds.merge("time")
        depths = nc.open_data("data/matchpoint_depths.nc")
        # ds.subset(time = 0)
        ds.append(depths)
        ds.merge()
        ds.regrid(pd.DataFrame({"lon":[1, 2], "lat":[54.5, 54.7]}), method = "bil")


        df = ds.to_dataframe().reset_index()
        df["month" ] =  [x.month for x in df.time_counter]
        df["year"] = [x.year for x in df.time_counter]
        df["day"] = [x.day for x in df.time_counter]
        df = df.loc[:,["lon", "lat", "month", "day", "year", "N3_n", "depth"]].drop_duplicates()
        ds = nc.open_data("data/matchpoint/*.nc")
        matcher = nc.open_matchpoint()
        matcher.add_data(ds, depths = depths)
        matcher.add_points(df.drop(columns = "N3_n"))
        matcher.matchup()


        assert matcher.values.rename(columns = {"N3_n":"nitrate"}).merge( df).assign(bias = lambda x: np.abs(x.N3_n - x.nitrate)).bias.max() < 0.0001
        assert len(matcher.values) == len(df)


        print("test 4")
        ds = nc.open_data("data/emodnet_test.nc")
        ds.regrid(pd.DataFrame({"lon": [0.15, 0.175], "lat" : [54.1, 54.12]}) )
        df = ds.to_dataframe().reset_index()
        ds = nc.open_data("data/emodnet_test.nc")
        matcher = nc.open_matchpoint()
        matcher.add_data(ds)
        matcher.add_points(df.loc[:,["lon", "lat"]])
        matcher.matchup()
        assert matcher.values.rename(columns = {"elevation":"values_123"}).merge(df).assign(bias = lambda x: np.abs(x.values_123 - x.elevation)).bias.max() < 0.00001

        assert len(matcher.values) == len(df)





        print("test 5")

        ds = nc.open_data(ensemble[0])
        ds.subset(time = 0)
        depths = nc.open_data("data/matchpoint_depths.nc")
        # ds.subset(time = 0)
        ds.append(depths)
        ds.merge()
        ds.regrid(pd.DataFrame({"lon":[1, 2], "lat":[54.5, 54.7]}), method = "bil")


        df = ds.to_dataframe().reset_index()
        df["month" ] =  [x.month for x in df.time_counter]
        df["year"] = [x.year for x in df.time_counter]
        df["day"] = [x.day for x in df.time_counter]
        df = df.loc[:,["lon", "lat", "month", "day", "year", "N3_n", "depth"]].drop_duplicates()
        ds = nc.open_data(ensemble[0])
        ds.subset(time = 0)
        matcher = nc.open_matchpoint()
        matcher.add_data(ds, depths = depths)
        matcher.add_points(df.drop(columns = "N3_n"))



        matcher.matchup()

        assert matcher.values.rename(columns = {"N3_n":"nitrate"}).merge( df).assign(bias = lambda x: np.abs(x.N3_n - x.nitrate)).bias.max() < 0.0001
        assert len(matcher.values) == len(df)

        print("test 6")

        ds = nc.open_data("data/sst.mon.mean.nc")
        df = pd.DataFrame({"lon":[-20], "lat":60})

        matcher = nc.open_matchpoint()
        matcher.add_points(df.loc[:,["lon", "lat"]])
        matcher.add_data(ds)
        matcher.matchup()
        matcher.values
        ds.regrid(df)
        df_test = ds.to_dataframe().reset_index().drop_duplicates()
        df_test["month"] = [x.month for x in df_test.time]
        df_test["day"] = [x.day for x in df_test.time]
        df_test["year"] = [x.year for x in df_test.time]
        assert df_test.rename(columns = {"sst":"test"}).merge(matcher.values).assign(bias = lambda x: np.abs(x.sst - x.test)).bias.max() <  0.00001
        assert len(matcher.values) == 360


        print("test 7")
        ds = nc.open_data("data/sst.mon.mean.nc")
        df = pd.DataFrame({"lon":[-20], "lat":60})

        matcher = nc.open_matchpoint()
        matcher.add_data(ds)
        matcher.add_points(df.loc[:,["lon", "lat"]])
        matcher.matchup()
        matcher.values
        ds.regrid(df)
        df_test = ds.to_dataframe().reset_index().drop_duplicates()
        df_test["month"] = [x.month for x in df_test.time]
        df_test["day"] = [x.day for x in df_test.time]
        df_test["year"] = [x.year for x in df_test.time]
        assert df_test.rename(columns = {"sst":"test"}).merge(matcher.values).assign(bias = lambda x: np.abs(x.sst - x.test)).bias.max() <  0.00001
        assert len(matcher.values) == 360



        print("test 8")
        ds = nc.open_data("data/matchpoint/amm7_1d_20000101_20000131_ptrc_T.nc")
        df = pd.DataFrame({"lon":[1.5], "lat":[55], "depth":[2.117196798324585]})
        depths = nc.open_data("data/matchpoint_depths.nc")
        matcher = nc.open_matchpoint()
        matcher.add_data(ds, depths = depths)
        matcher.add_points(df.loc[:,["lon", "lat", "depth"]])
        matcher.matchup()
        ds = nc.open_data("data/matchpoint/amm7_1d_20000101_20000131_ptrc_T.nc")
        depths = nc.open_data("data/matchpoint_depths.nc")
        ds.append(depths)
        ds.regrid(df)
        ds.merge()
        df_test = ds.to_dataframe().reset_index().loc[:,["lon", "lat", "depth", "N3_n", "time_counter"]].drop_duplicates().query("depth == 2.117196798324585")
        df_test["day"] = [x.day for x in df_test.time_counter]
        df_test["month"] = [x.month for x in df_test.time_counter]
        df_test["year"] = [x.year for x in df_test.time_counter]
        df_test = df_test.loc[:,["lon", "lat", "depth", "day", "month", "year", "N3_n"]].rename(columns = {"N3_n":"test"}).reset_index(drop = True)
        assert df_test.merge(matcher.values).assign(bias = lambda x: np.abs(x.test - x.N3_n)).bias.max() <  0.00001
        assert len(df_test) == 31


        print("test 10")


        ds = nc.open_data("data/matchpoint/amm7_1d_20000101_20000131_ptrc_T.nc")
        df = pd.DataFrame({"lon":[1.5], "lat":[55], "depth":[2.117196798324585]})
        depths = nc.open_data("data/matchpoint_depths.nc")
        matcher = ds.match_points(df.loc[:,["lon", "lat", "depth"]], depths = depths)

        ds = nc.open_data("data/matchpoint/amm7_1d_20000101_20000131_ptrc_T.nc")
        depths = nc.open_data("data/matchpoint_depths.nc")
        ds.append(depths)
        ds.regrid(df)
        ds.merge()
        df_test = ds.to_dataframe().reset_index().loc[:,["lon", "lat", "depth", "N3_n", "time_counter"]].drop_duplicates().query("depth == 2.117196798324585")
        df_test["day"] = [x.day for x in df_test.time_counter]
        df_test["month"] = [x.month for x in df_test.time_counter]
        df_test["year"] = [x.year for x in df_test.time_counter]
        df_test = df_test.loc[:,["lon", "lat", "depth", "day", "month", "year", "N3_n"]].rename(columns = {"N3_n":"test"}).reset_index(drop = True)
        assert df_test.merge(matcher).assign(bias = lambda x: np.abs(x.test - x.N3_n)).bias.max() <  0.00001
        assert len(df_test) == 31


        ds = nc.open_data("data/matchpoint/*.nc", checks = False)
        depths = nc.open_data("data/matchpoint_depths.nc")
        df = pd.DataFrame({"lon":[0.5, 0.7], "lat":[55,55], "day": [2,2],  "month":[1, 2], "depth": 2})
        df_res = ds.match_points(df, depths = depths)
        assert  len(df_res.merge(df)) == 2

        ds = nc.open_data("data/matchpoint/*.nc", checks = False)
        depths = nc.open_data("data/matchpoint_depths.nc")
        df = pd.DataFrame({"lon":[0.5, 0.7], "lat":[55,55], "day": [2,2],  "month":[1, 2]})
        df_res = ds.match_points(df, depths = depths)
        assert len(df_res.merge(df))  == 2 * 51

        ds = nc.open_data("data/woa18_decav_t01_01.nc")
        df = pd.DataFrame({"lon":np.repeat(-20, 8), "lat":np.repeat(55, 8), "depth":np.arange(-7, 1)})
        df_matched = ds.match_points(df, max_extrap=6)
        assert np.isnan(df_matched.query("depth == -7").t_an[0])
        assert df_matched.query("depth == -5").t_an.values[0] == df_matched.query("depth == 0").t_an.values[0]

