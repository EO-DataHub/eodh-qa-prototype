import plotly.graph_objects as go
import numpy as np
import pandas as pd
import random
import xarray as xr

from natsort import natsorted
from datetime import datetime

import requests
import json

sat_name = {
    "s2": "Sentinel-2",
    "s2a": "Sentinel-2A",
    "s2b": "Sentinel-2B",
    "l8": "Landsat 8",
    "planet": "Planet SuperDove",
    "airbus_phr": "Airbus Pleiades",
}
ref_name = {
    "RCN-GONA": "RadCalNet - GONA",
    "RCN-RVUS": "RadCalNet - RVUS",
    "LIBYA-4": "PICS - Libya-4",
    "PICS - LIBYA-1": "Libya-1",
    "ceos-virtual-ref": "CEOS Virtual Reference",
    "HYP-GHNA": "HYPERNETS - GHNA",
}


# number the bands - be aware for S2 B8A onwards not aligned with band numbers, ie 442=B1, 864=B8A, 1613=B11
s2_bands_idx = {
    "442 nm": 0,
    "492 nm": 1,
    "559 nm": 2,
    "664 nm": 3,
    "704 nm": 4,
    "740 nm": 5,
    "782 nm": 6,
    "832 nm": 7,
    "864 nm": 8,
    "945 nm": 9,
    "1373 nm": 10,
    "1613 nm": 11,
}

planet_bands_idx = {
    "442 nm": 0,
    "490 nm": 1,
    "531 nm": 2,
    "565 nm": 3,
    "610 nm": 4,
    "665 nm": 5,
    "705 nm": 6,
    "865 nm": 7,
}

airbus_bands_idx = {"490 nm": 0, "560 nm": 1, "650 nm": 2, "840 nm": 3}

l8_bands_idx = {
    "444 nm": 0,
    "458 nm": 1,
    "560 nm": 2,
    "650 nm": 3,
    "860 nm": 4,
    "1610 nm": 5,
    "2200 nm": 6,
    "590 nm": 7,
    "1380 nm": 8,
}

dummy_AOD = np.array(
    [
        0.131,
        0.151,
        0.154,
        0.088,
        0.092,
        0.096,
        0.096,
        0.110,
        0.126,
        0.121,
        0.112,
        0.103,
        0.100,
        0.070,
        0.070,
        0.063,
        0.061,
        0.058,
        0.060,
        0.059,
        0.054,
        0.052,
        0.050,
        0.052,
        0.062,
        0.057,
        0.014,
        0.014,
        0.014,
        0.013,
        0.013,
        0.013,
        0.014,
        0.013,
        0.012,
        0.013,
        0.013,
        0.015,
        0.015,
    ]
)

dummy_temp = np.array([])
dummy_cloud_percent = np.array([0, 0, 0, 0, 0, 0, 0, 0, 2, 3, 4, 9, 15, 0, 0, 0, 3, 2])
dummy_sun_azimuth = np.array(
    [
        97.5,
        97.3,
        94.6,
        94.3,
        97.4,
        97.1,
        97.3,
        93.9,
        96.5,
        92.6,
        95.8,
        91.7,
        85.6,
        89.4,
        85.2,
        88.6,
        85.5,
        81.7,
        81.5,
        85.7,
        77.3,
        77.4,
        76.8,
        76.6,
        74.0,
    ]
)
dummy_sun_elevation = np.array(
    [
        51.7,
        61.8,
        51.7,
        61.8,
        53.7,
        64.8,
        53.7,
        64.8,
        56.2,
        60.5,
        56.2,
        61.5,
        56.3,
        60.3,
        55.8,
        61.8,
        54.4,
        63.9,
        52.2,
        58.5,
    ]
)
dummy_sat_view_angle = np.array(
    [
        5.0,
        1.0,
        5.0,
        4.1,
        2.0,
        4.9,
        4.9,
        5.0,
        2.0,
        0.1,
        2.0,
        5.1,
        1.9,
        5.0,
        4.0,
        1.1,
        2.1,
        0.2,
        0.2,
        2.0,
        2.0,
        2.0,
        5.0,
        5.0,
        1.7,
    ]
)


# access db for given selection and extract corresponding matchups
def extract_mup_info_from_db(sensor1: str, sensor2: list, dates: list):

    # get matchups for that time period from db api
    mup_info = xr.Dataset({})

    # for idx, ref in enumerate(sensor2):
    if dates[0].strftime("%Y-%m-%d") == dates[1].strftime("%Y-%m-%d"):
        daterange = (
            dates[0].strftime("%Y-%m-%dT%H:%M")
            + ","
            + dates[1].strftime("%Y-%m-%dT%H:%M")
        )
    else:
        daterange = dates[0].strftime("%Y-%m-%d") + "," + dates[1].strftime("%Y-%m-%d")

    if sensor1 == "s2":  # return S-2A by default if S2 is called
        sensor1 = "s2a"

    url_sensor2 = None
    if len(sensor2) == 1:
        url_sensor2 = sensor2[0]
    elif len(sensor2) == 2:
        url_sensor2 = sensor2[0] + "," + sensor2[1]

    if url_sensor2 != None:
        url = f"http://db-api.eba-3ean8bmb.eu-west-2.elasticbeanstalk.com/matchups?sensor1={sensor1}&sensor2={url_sensor2}&dates={daterange}"
        response = requests.get(url)
        mup_dict = json.loads(response.text)
        mup_ds = xr.Dataset.from_dict(mup_dict)

        refs_list = []
        for attr in mup_ds.attrs:
            if "Datetime" in attr:
                refs_list.append(attr.split("_")[-2])

        for idx, ref in enumerate(refs_list):
            if mup_ds:
                # overwrite bias unc vals for now
                bias_unc_vals = np.ones((13, 1)) * 0.02
                for k in range(len(mup_ds.attrs[f"{sensor1}_{ref}_Datetime"])):
                    mup_ds[str(sensor1) + "_" + str(ref) + "_BiasUncVals"].values[k] = (
                        xr.DataArray(data=bias_unc_vals.flatten())
                    )

        if mup_ds:
            mup_info = xr.merge([mup_info, mup_ds], combine_attrs="no_conflicts")

        for idx, ref in enumerate(
            refs_list
        ):  # replacing metadata with dummy values for now - todo: update once all db metadata inputs are in for all sats
            for mup_id in mup_info.attrs[str(sensor1) + "_" + str(ref) + "_MatchupIDs"]:
                mup_info.attrs[str(sensor1) + "_" + str(ref) + "_Metadata"][mup_id][
                    "Satellite Viewing Angle"
                ] = (str(random.choice(dummy_sat_view_angle)) + "°")
                mup_info.attrs[str(sensor1) + "_" + str(ref) + "_Metadata"][mup_id][
                    "Solar Azimuth Angle"
                ] = (str(random.choice(dummy_sun_azimuth)) + "°")
                mup_info.attrs[str(sensor1) + "_" + str(ref) + "_Metadata"][mup_id][
                    "Solar Elevation Angle"
                ] = (str(random.choice(dummy_sun_elevation)) + "°")

    return mup_info


# return timeseries data for plotting, per ref site selected - currently only works for max 2 ref sites
def return_timeseries_data(sat, refs, band, dates):
    bands = natsorted(band)
    sel_refs = sorted(refs)
    refs = []

    date_range = [
        datetime.strptime(dates[0], "%Y-%m-%d"),
        datetime.strptime(
            dates[1], "%Y-%m-%d"
        ),  # add a day to make sure its inclusive (i.e. until midnight that day)
    ]

    timeseries_data_all_bands = extract_mup_info_from_db(sat, sel_refs, date_range)
    for ref in sel_refs:
        if ref in str(timeseries_data_all_bands.attrs.keys()):
            refs.append(ref)
    empty_df = pd.DataFrame(
        columns=[
            "Ref",
            "Datetime",
            "BiasVals",
            "BiasUncVals",
            "MeasValsSensor1",
            "MeasValsSensor2",
        ]
    )
    if not timeseries_data_all_bands.data_vars:
        return empty_df, empty_df

    timeseries_data_all_bands.copy()

    # output the timeseries data as df for plotting
    if sat == "planet":
        bands_idx = planet_bands_idx
    elif sat in [
        "s2",
        "s2a",
        "s2b",
    ]:
        bands_idx = s2_bands_idx
    elif sat == "l8":
        bands_idx = l8_bands_idx
    elif sat == "airbus_phr":
        bands_idx = airbus_bands_idx

    clicked_band_idx = []
    for bnd in bands:
        if bnd in bands_idx.keys():
            clicked_band_idx.append(bands_idx[bnd])
        else:
            return empty_df, empty_df

    timeseries_data_ref1 = pd.DataFrame(
        index=range(
            timeseries_data_all_bands.data_vars[
                str(sat) + "_" + str(refs[0]) + "_BiasVals"
            ].values.shape[0]
        ),
        columns=[
            "Ref",
            "Datetime",
            "BiasVals",
            "BiasUncVals",
            "MeasValsSensor1",
            "MeasValsSensor2",
        ],
    )

    for i in range(len(timeseries_data_ref1.index)):
        timeseries_data_ref1["Ref"] = refs[0]
        timeseries_data_ref1["Datetime"].iloc[i] = timeseries_data_all_bands.attrs[
            str(sat) + "_" + str(refs[0]) + "_Datetime"
        ][i]
        timeseries_data_ref1["BiasVals"].iloc[i] = timeseries_data_all_bands.data_vars[
            str(sat) + "_" + str(refs[0]) + "_BiasVals"
        ].values[i][[clicked_band_idx]]
        timeseries_data_ref1["BiasUncVals"].iloc[i] = (
            timeseries_data_all_bands.data_vars[
                str(sat) + "_" + str(refs[0]) + "_BiasUncVals"
            ].values[i][[clicked_band_idx]]
        )
        timeseries_data_ref1["MeasValsSensor1"].iloc[i] = (
            timeseries_data_all_bands.data_vars[
                str(sat) + "_" + str(refs[0]) + "_MeasValsSensor1"
            ].values[i][[clicked_band_idx]]
        )
        timeseries_data_ref1["MeasValsSensor2"].iloc[i] = (
            timeseries_data_all_bands.data_vars[
                str(sat) + "_" + str(refs[0]) + "_MeasValsSensor2"
            ].values[i][[clicked_band_idx]]
        )

    if len(refs) > 1:
        timeseries_data_ref2 = pd.DataFrame(
            index=range(
                timeseries_data_all_bands.data_vars[
                    str(sat) + "_" + str(refs[1]) + "_BiasVals"
                ].values.shape[0]
            ),
            columns=[
                "Ref",
                "Datetime",
                "BiasVals",
                "BiasUncVals",
                "MeasValsSensor1",
                "MeasValsSensor2",
            ],
        )

        for i in range(len(timeseries_data_ref2.index)):
            timeseries_data_ref2["Ref"] = refs[1]
            timeseries_data_ref2["Datetime"].iloc[i] = timeseries_data_all_bands.attrs[
                str(sat) + "_" + str(refs[1]) + "_Datetime"
            ][i]
            timeseries_data_ref2["BiasVals"].iloc[i] = (
                timeseries_data_all_bands.data_vars[
                    str(sat) + "_" + str(refs[1]) + "_BiasVals"
                ].values[i][[clicked_band_idx]]
            )
            timeseries_data_ref2["BiasUncVals"].iloc[i] = (
                timeseries_data_all_bands.data_vars[
                    str(sat) + "_" + str(refs[1]) + "_BiasUncVals"
                ].values[i][[clicked_band_idx]]
            )
            timeseries_data_ref2["MeasValsSensor1"].iloc[i] = (
                timeseries_data_all_bands.data_vars[
                    str(sat) + "_" + str(refs[1]) + "_MeasValsSensor1"
                ].values[i][[clicked_band_idx]]
            )
            timeseries_data_ref2["MeasValsSensor2"].iloc[i] = (
                timeseries_data_all_bands.data_vars[
                    str(sat) + "_" + str(refs[1]) + "_MeasValsSensor2"
                ].values[i][[clicked_band_idx]]
            )
    else:
        timeseries_data_ref2 = pd.DataFrame(
            index=range(
                timeseries_data_all_bands.data_vars[
                    str(sat) + "_" + str(refs[0]) + "_BiasVals"
                ].values.shape[0]
            ),
            columns=[
                "Ref",
                "Datetime",
                "BiasVals",
                "BiasUncVals",
                "MeasValsSensor1",
                "MeasValsSensor2",
            ],
        )
    return (
        timeseries_data_ref1,
        timeseries_data_ref2,
    )  # todo: update to do this for ref in refs - when >2 refs are chosen


# plot upper plot timeseries data
def plot_timeseries(
    sat,
    band,
    refs,
    date_df_r1,
    bias_r1,
    bias_unc_r1,
    meas_vals_r1,
    date_df_r2,
    bias_r2,
    bias_unc_r2,
    meas_vals_r2,
    hyp_bias=None,
    hyp_bias_unc=None,
):

    bands = natsorted(band)
    refs = sorted(refs)

    if date_df_r2.isnull().iloc[0]:
        refs = [refs[0]]

    bias_vals_r1 = np.ones((len(bands), len(date_df_r1))) * np.nan
    bias_unc_vals_r1 = np.ones((len(bands), len(date_df_r1))) * np.nan
    rcn_meas_vals_r1 = np.ones((len(bands), len(date_df_r1))) * np.nan
    bias_vals_r2 = np.ones((len(bands), len(date_df_r2))) * np.nan
    bias_unc_vals_r2 = np.ones((len(bands), len(date_df_r2))) * np.nan
    rcn_meas_vals_r2 = np.ones((len(bands), len(date_df_r2))) * np.nan

    # reorder bias and bias unc vals to per band
    for i in range(len(date_df_r1)):
        for k in range(len(bands)):
            bias_vals_r1[k][i] = bias_r1.values[i].flatten()[k]
            bias_unc_vals_r1[k][i] = bias_unc_r1.values[i].flatten()[k]
            rcn_meas_vals_r1[k][i] = meas_vals_r1.values[i].flatten()[k]

    if len(refs) > 1:
        for i in range(len(date_df_r2)):
            for k in range(len(bands)):
                bias_vals_r2[k][i] = bias_r2.values[i].flatten()[k]
                bias_unc_vals_r2[k][i] = bias_unc_r2.values[i].flatten()[k]
                rcn_meas_vals_r2[k][i] = meas_vals_r2.values[i].flatten()[k]

    bias_percentage_r1 = np.ones(bias_vals_r1.shape) * np.nan
    bias_percentage_r2 = np.ones(bias_vals_r2.shape) * np.nan

    for k in range(len(bands)):
        bias_percentage_r1[k] = bias_vals_r1[k] / rcn_meas_vals_r1[k] * 100
        bias_percentage_r2[k] = bias_vals_r2[k] / rcn_meas_vals_r2[k] * 100

    # # remove 100% outliers as means no data from sat - removes all if one band has 100% - leave for now
    # ref_1_idx_rem = []
    # ref_2_idx_rem = []
    # for i in range(len(bands)):
    #     for j in range(len(date_df_r1)):
    #         if bias_percentage_r1[i][j] == 100:
    #             ref_1_idx_rem.append(j)
    #     for j in range(len(date_df_r2)):
    #         if bias_percentage_r2[i][j] == 100:
    #             ref_2_idx_rem.append(j)
    # for i in range(len(bands)):
    #     for idx in ref_1_idx_rem:
    #         date_df_r1[idx] = np.nan
    #         bias_percentage_r1[i][idx] = np.nan
    #     for idx in ref_2_idx_rem:
    #         date_df_r2[idx] = np.nan
    #         bias_percentage_r2[i][idx] = np.nan

    legend_ref = refs
    for idx, ref in enumerate(refs):
        if ref == "ceos-virtual-ref":
            legend_ref[idx] = "Ceos Virtual Ref"

    fig_2 = go.Figure()

    for i in range(len(bands)):
        fig_2.add_trace(
            go.Scatter(
                x=date_df_r1,
                y=bias_percentage_r1[i],
                mode="lines+markers",
                name=bands[i],
                error_y_array=bias_unc_vals_r1[i],
                legendgroup="group1",
                legendgrouptitle_text=f"{legend_ref[0]}",
            )
        )
        if len(refs) > 1:
            fig_2.add_trace(
                go.Scatter(
                    x=date_df_r2,
                    y=bias_percentage_r2[i],
                    mode="lines+markers",
                    name=bands[i],
                    error_y_array=bias_unc_vals_r2[i],
                    legendgroup="group2",
                    legendgrouptitle_text=f"{legend_ref[-1]}",
                )
            )

    fig_2.update_traces(
        line=dict(dash="dash", width=0),
        marker=dict(size=10, symbol="hexagon"),
        showlegend=True,
    )
    fig_2.update_layout(
        clickmode="event+select",
        # title={
        #     'text': f"{rcn_site} and {hyp_site} Sites Compared with {sat}",
        #     'x': 0.5,
        #     'xanchor': 'center',
        #     'yanchor': 'top'},
        legend_title_text=sat_name[str(sat)] + "<br>Wavelengths",
        legend=dict(groupclick="toggleitem"),  # "togglegroup"
    )
    fig_2.layout.margin = {"t": 10, "b": 10, "r": 0, "l": 20}
    fig_2.update_yaxes(
        title={"text": "Percentage Difference", "font.size": 15},
        tickfont_size=15,
        griddash="solid",
        gridwidth=2,
        linewidth=2,
        linecolor="navy",
        minor={
            "griddash": "solid",
            "nticks": 5,
            "gridcolor": "white",  # aquamarine #aliceblue
            "gridwidth": 0.5,
        },
    )
    fig_2.update_xaxes(
        # tickangle=90,
        title={"text": "Date", "font.size": 15},
        tickfont_size=15,
        linewidth=2,
        linecolor="navy",
    )

    return fig_2


# populate upper panel table with mean bias vals
def get_bias_table_vals(
    sat,
    refs,
    bands,
    date_df_r1,
    bias_r1,
    bias_unc_r1,
    meas_vals_r1,
    date_df_r2=None,
    bias_r2=None,
    bias_unc_r2=None,
    meas_vals_r2=None,
):  # todo: update to take in refs (not each refs bias) and get bias from that
    bias_vals = {}
    band = natsorted(bands)
    refs = sorted(refs)

    if date_df_r2.isnull().iloc[0]:
        refs = [refs[0]]

    bias_vals_r1 = np.ones((len(band), len(date_df_r1))) * np.nan
    bias_unc_vals_r1 = np.ones((len(band), len(date_df_r1))) * np.nan
    rcn_meas_vals_r1 = np.ones((len(band), len(date_df_r1))) * np.nan
    bias_vals_r2 = np.ones((len(band), len(date_df_r2))) * np.nan
    bias_unc_vals_r2 = np.ones((len(band), len(date_df_r2))) * np.nan
    rcn_meas_vals_r2 = np.ones((len(band), len(date_df_r2))) * np.nan

    # extract and reorder bias and bias unc vals to per band, per site
    for i in range(len(date_df_r1)):
        for k in range(len(bands)):
            bias_vals_r1[k][i] = bias_r1.values[i].flatten()[k]
            bias_unc_vals_r1[k][i] = bias_unc_r1.values[i].flatten()[k]
            rcn_meas_vals_r1[k][i] = meas_vals_r1.values[i].flatten()[k]

    if len(refs) > 1:
        for i in range(len(date_df_r2)):
            for k in range(len(bands)):
                bias_vals_r2[k][i] = bias_r2.values[i].flatten()[k]
                bias_unc_vals_r2[k][i] = bias_unc_r2.values[i].flatten()[k]
                rcn_meas_vals_r2[k][i] = meas_vals_r2.values[i].flatten()[k]

    bias_percentage_r1 = np.ones(bias_vals_r1.shape) * np.nan
    bias_percentage_r2 = np.ones(bias_vals_r2.shape) * np.nan

    # calculate bias percentage
    for k in range(len(bands)):
        bias_percentage_r1[k] = bias_vals_r1[k] / rcn_meas_vals_r1[k] * 100
        bias_percentage_r2[k] = bias_vals_r2[k] / rcn_meas_vals_r2[k] * 100

    bias_vals_mean_r1 = []
    bias_vals_mean_r2 = []

    for k in range(len(bias_vals_r1)):
        bias_vals_mean_r1.append(
            round(
                sum(bias_percentage_r1[k][~np.isnan(bias_percentage_r1[k])])
                / len(bias_percentage_r1[k][~np.isnan(bias_percentage_r1[k])]),
                2,
            )
        )
        if len(refs) > 1:
            bias_vals_mean_r2.append(
                round(
                    sum(bias_percentage_r2[k][~np.isnan(bias_percentage_r2[k])])
                    / len(bias_percentage_r2[k][~np.isnan(bias_percentage_r2[k])]),
                    2,
                )
            )

    # find relevant bands and order based on sat
    for ref in refs:
        if ref == refs[0]:
            rcn_bias_vals_mean = bias_vals_mean_r1
        else:
            rcn_bias_vals_mean = bias_vals_mean_r2

        table_ref = ref
        if ref == "ceos-virtual-ref":
            table_ref = "Ceos Virtual Ref"

        for k in range(len(band)):
            if sat == "planet":
                bias_vals[
                    table_ref
                    + " B"
                    + str(planet_bands_idx[band[k]] + 1)
                    + " - "
                    + str(band[k])
                ] = f"{rcn_bias_vals_mean[k]}%"
            elif sat == "airbus_phr":
                bias_vals[
                    table_ref
                    + " B"
                    + str(airbus_bands_idx[band[k]] + 1)
                    + " - "
                    + str(band[k])
                ] = f"{rcn_bias_vals_mean[k]}%"
            elif sat == "l8":
                bias_vals[
                    table_ref
                    + " B"
                    + str(l8_bands_idx[band[k]] + 1)
                    + " - "
                    + str(band[k])
                ] = f"{rcn_bias_vals_mean[k]}%"
            elif sat in ["s2a", "s2b", "s2"]:
                if s2_bands_idx[band[k]] <= 7:
                    bias_vals[
                        table_ref
                        + " B"
                        + str(s2_bands_idx[band[k]] + 1)
                        + " - "
                        + str(band[k])
                    ] = f"{rcn_bias_vals_mean[k]}%"
                elif s2_bands_idx[band[k]] == 8:
                    bias_vals[table_ref + " B8A" + " - " + str(band[k])] = (
                        f"{rcn_bias_vals_mean[k]}%"
                    )
                else:
                    bias_vals[
                        table_ref
                        + " B"
                        + str(s2_bands_idx[band[k]])
                        + " - "
                        + str(band[k])
                    ] = f"{rcn_bias_vals_mean[k]}%"

    bias_vals_sorted = dict(natsorted(bias_vals.items()))

    for k, v in bias_vals_sorted.items():
        if v == "-0.0%":
            bias_vals_sorted[k] = "0.0%"

    return bias_vals_sorted


# populate matchup analysis table
def analysis_table_update(sat, refs, mup_info):

    col_1 = []
    col_2 = []

    # extract metadata for analysis table and convert to correct format for input
    for key in mup_info.attrs[f"{sat}_{refs[0]}_Metadata"].keys():
        mup_id = key
    for k, v in mup_info.attrs[f"{sat}_{refs[0]}_Metadata"][mup_id].items():
        if k not in ["Mission Product", "Reference Product"]:
            if k in ["Mission Date & Time"]:
                col_1.append(k)
                col_2.append(v.split("T")[0] + " " + v.split("T")[1].split(".")[0])
            else:
                col_1.append(k)
                col_2.append(v)

    for i, val in enumerate(col_2):

        if isinstance(val, datetime):
            col_2[i] = val.strftime("%Y-%m-%d %H:%M:%S")

    matchup_analysis_df = pd.DataFrame(
        data={
            "column_1": col_1,
            "column_2": col_2,
        },
        index=range(len(col_1)),
    )

    matchup_analysis_df.loc[0, "column_2"] = sat_name[sat] + " & " + ref_name[refs[0]]

    matchup_analysis = matchup_analysis_df.to_dict("records"), [
        {"name": i, "id": i} for i in matchup_analysis_df.columns
    ]

    return matchup_analysis


# make small plot for bottom panel
def small_plot_update(sat, refs, mup_info):

    ref = refs[0]

    # reorder indices so that for S-2 B8A (with corresponding data) slots in between B8-B9
    sensor_1_meas_vals = mup_info.data_vars[
        f"{sat}_{ref}_MeasValsSensor1"
    ].values.flatten()
    sensor_2_meas_vals = mup_info.data_vars[
        f"{sat}_{ref}_MeasValsSensor2"
    ].values.flatten()
    sensor_1_wav_vals = mup_info.attrs[f"{sat}_{ref}_CentralWavelengthsSensor1"]
    # sensor_2_wav_vals = mup_info['CentralWavelengthsSensor1']

    sensor_1_meas_vals[sensor_1_meas_vals == -9999] = np.nan
    sensor_2_meas_vals[sensor_2_meas_vals == -9999] = np.nan
    sensor_1_wav_vals[sensor_1_wav_vals == -9999] = np.nan

    # if s2 - display only 5 bands
    if sat in ["s2", "s2a", "s2b"]:
        sensor_1_meas_vals = sensor_1_meas_vals[0:5]
        sensor_2_meas_vals = sensor_2_meas_vals[0:5]

    # todo: check if will always be input in order
    sensor_1_wav_sort = sensor_1_wav_vals
    # sensor1_wav_idx = np.argsort(sensor_1_wav_vals)
    # sensor_1_wav_sort = sensor_1_wav_vals[sensor1_wav_idx][0]
    # sensor_1_meas_vals_sort = sensor_1_meas_vals[sensor1_wav_idx][0].flatten()
    # sensor_2_meas_vals_sort = sensor_2_meas_vals[sensor1_wav_idx][0].flatten()

    for i, val in enumerate(sensor_1_wav_sort):
        if isinstance(val, str):
            sensor_1_wav_sort[i] = val.split(".")[0]

    fig_small = go.Figure()
    fig_small.add_trace(
        go.Scatter(
            x=sensor_1_wav_sort,
            y=sensor_1_meas_vals,
            mode="lines+markers",
            name=sat_name[sat],
        )
    )
    # line_color=color_group[i],
    # marker_color=color_group[i]))
    fig_small.add_trace(
        go.Scatter(
            x=sensor_1_wav_sort,
            y=sensor_2_meas_vals,
            mode="lines+markers",
            name=ref_name[ref],
        )
    )
    fig_small.update_traces(
        line=dict(dash="dash", width=2), marker=dict(size=10), showlegend=True
    )
    fig_small.update_layout(
        legend=dict(x=0, y=1, xanchor="left", yanchor="top", bgcolor="rgba(0,0,0,0)"),
    )
    fig_small.layout.margin = {"t": 10, "b": 10, "r": 0, "l": 20}
    fig_small.update_yaxes(
        title={"text": "Reflectance", "font.size": 15},
        tickfont_size=15,
        linewidth=2,
        linecolor="navy",
        minor={
            "griddash": "solid",
            "nticks": 5,
            "gridcolor": "white",  # aquamarine #aliceblue
            "gridwidth": 0.5,
        },
    )
    fig_small.update_xaxes(
        tickangle=60,
        title={"text": "Wavelength", "font.size": 15},
        tickfont_size=15,
        linewidth=2,
        linecolor="navy",
    )

    return fig_small


if __name__ == "__main__":
    pass
