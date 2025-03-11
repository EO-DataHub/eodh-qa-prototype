import plotly.graph_objects as go
import numpy as np
import pandas as pd
import xarray as xr

from natsort import natsorted
from datetime import datetime


from sqlalchemy import create_engine, MetaData
from database.config import DATABASE_URI
from database.models import Base, Matchup, ReferenceSite, Collection, BiasVals, BiasUncVals, MeasVals
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

engine = create_engine(DATABASE_URI)

Session = sessionmaker(bind=engine)  # , autoflush=False)

# manage connection to db
@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

# dict to align sats/refs with corresponding ids in db
with session_scope() as s:
    id_dict = {}
    for ref in s.query(ReferenceSite).all():
        id_dict[ref.site_name] = ref.id
    for coll in s.query(Collection).all():
        id_dict[coll.collection] = coll.id


sat_name = {'s2': 'Sentinel-2','s2a': 'Sentinel-2A', 's2b': 'Sentinel-2B', 'l8': 'Landsat 8',
            'planet': 'Planet SuperDove', 'airbus_phr': 'Airbus Pleiades'}
ref_name = {'RCN-GONA': 'RadCalNet - GONA', 'RCN-RVUS': 'RadCalNet - RVUS', 'HYP-GHNA': 'HYPERNETS - GHNA'}


# number the bands - be aware for S2 B8A onwards not aligned with band numbers, ie 442=B1, 864=B8A, 1613=B11
s2_bands_idx = {'442 nm': 0, '492 nm': 1, '559 nm': 2, '664 nm': 3, '704 nm': 4, '740 nm': 5,
               '782 nm': 6, '832 nm': 7, '864 nm': 8, '945 nm': 9, '1373 nm': 10, '1613 nm': 11}

# s2a_bands_idx = {'443 nm': 0, '492 nm': 1, '560 nm': 2, '665 nm': 3, '704 nm': 4, '741 nm': 5,
#                  '783 nm': 6, '833 nm': 7, '865 nm': 8, '945 nm': 9, '1374 nm': 10, '1614 nm': 11, '2202 nm': 12}
#
# s2b_bands_idx = {'442 nm': 0, '492 nm': 1, '559 nm': 2, '665 nm': 3, '704 nm': 4, '739 nm': 5,
#                  '780 nm': 6, '833 nm': 7, '864 nm': 8, '943 nm': 9, '1377 nm': 10, '1610 nm': 11, '2186 nm': 12}

planet_bands_idx = {'442 nm': 0, '490 nm': 1, '531 nm': 2, '565 nm': 3, '610 nm': 4, '665 nm': 5, '705 nm': 6, '865 nm': 7}

airbus_bands_idx = {'490 nm': 0, '560 nm': 1, '650 nm': 2, '840 nm': 3}

l8_bands_idx = {'444 nm': 0, '458 nm': 1, '560 nm': 2, '650 nm': 3, '860 nm': 4, '1610 nm': 5, '2200 nm': 6, '590 nm': 7, '1380 nm': 8}

# access db for given selection and extract corresponding matchups
def extract_mup_info_from_db(sensor1:str, sensor2:list, dates:list):

    # find ids of sat and refs selected
    if sensor1 == 's2':
        coll_idx = [id_dict[sat_name['s2a']], id_dict[sat_name[('s2b')]]]
    else:
        coll_idx = id_dict[sat_name[sensor1]]
    if len(sensor2) == 1:
        ref_idxs = [id_dict[ref_name[sensor2[0]]]]
    else:
        ref_idxs = []
        for ref in sensor2:
            ref_idxs.append(id_dict[ref_name[ref]])

    mup_info = xr.Dataset({})

    mups_list = [[]] * len(sensor2)

    # find and extract db matchups based on selection
    with session_scope() as s:
        for idx, ref in enumerate(sensor2):
            ref_idx = ref_idxs[idx]
            if sensor1 in 's2':
                for coll_id in coll_idx:
                    mups_list[idx] = mups_list[idx] + s.query(Matchup).where(Matchup.sensor_1_collection_id == coll_id).where(
                        Matchup.sensor_2_reference_id == ref_idx).where(Matchup.product_date.between(dates[0], dates[-1])).all()
            else:
                mups_list[idx] = mups_list[idx] + s.query(Matchup).where(Matchup.sensor_1_collection_id == coll_idx).where(Matchup.sensor_2_reference_id == ref_idx).where(Matchup.product_date.between(dates[0],dates[-1])).all()

        if not any(emp_list for emp_list in mups_list):
            mup_info = xr.Dataset({})
            return mup_info

        # create empty ds with correct attrs based on selected sat and refs
        for idx, ref in enumerate(sensor2):
            mup_info.attrs[str(sensor1) + '_' + str(ref) + '_Datetime'] = [[]] * len(mups_list[idx])
            mup_info.attrs[str(sensor1) + '_' + str(ref) + '_BandsSensor1'] = []
            mup_info.attrs[str(sensor1) + '_' + str(ref) + '_BandsSensor2'] = []
            mup_info.attrs[str(sensor1) + '_' + str(ref) + '_CentralWavelengthsSensor1'] = []
            mup_info.attrs[str(sensor1) + '_' + str(ref) + '_Metadata'] = {}
            mup_info[str(sensor1) + '_' + str(ref) + '_BiasVals'] = xr.DataArray(
                data=np.ones((len(mups_list[idx]), 13))*np.nan,
                attrs={},
                dims=['mups_'+str(idx+1),'bands'],
            )
            mup_info[str(sensor1) + '_' + str(ref) + '_BiasUncVals'] = xr.DataArray(
                data=np.ones((len(mups_list[idx]), 13))*np.nan,
                attrs={},
                dims=['mups_'+str(idx+1),'bands'],
            )
            mup_info[str(sensor1) + '_' + str(ref) + '_MeasValsSensor1'] = xr.DataArray(
                data=np.ones((len(mups_list[idx]), 13))*np.nan,
                attrs={},
                dims=['mups_'+str(idx+1),'bands'],
            )
            mup_info[str(sensor1) + '_' + str(ref) + '_MeasValsSensor2'] = xr.DataArray(
                data=np.ones((len(mups_list[idx]), 13))*np.nan,
                attrs={},
                dims=['mups_'+str(idx+1),'bands'],
            )

        # per matchup found in db, extract meas vals, bias vals and corresponding unc vals
        for idx, ref in enumerate(sensor2):
            mup_ids = []
            for k, mup in enumerate(mups_list[idx]):
                mup_idx = mup.id
                bias_vals_db = s.query(BiasVals).where(BiasVals.matchup_id == mup_idx).all()
                bias_unc_vals_db = s.query(BiasUncVals).where(BiasUncVals.matchup_id == mup_idx).all()
                meas_vals_dbs = s.query(MeasVals).where(MeasVals.matchup_id == mup_idx).all()
                for mup_meas_vals in meas_vals_dbs:
                    if mup_meas_vals.sensor_1_collection_id:
                        meas_vals_sensor1_db = mup_meas_vals
                    elif mup_meas_vals.sensor_2_collection_id:
                        meas_vals_sensor2_db = mup_meas_vals
                    elif mup_meas_vals.sensor_2_reference_id:
                        meas_vals_sensor2_db = mup_meas_vals

                bias_vals = np.ones((13, 1))*np.nan
                bias_unc_vals = np.ones((13, 1))*np.nan
                meas_vals_sensor1 = np.ones((13, 1))*np.nan
                meas_vals_sensor2 = np.ones((13, 1))*np.nan

                # must be done per band as current db tables do not support ndarrays
                bias_vals[0] = bias_vals_db[0].band_1
                bias_vals[1] = bias_vals_db[0].band_2
                bias_vals[2] = bias_vals_db[0].band_3
                bias_vals[3] = bias_vals_db[0].band_4
                bias_vals[4] = bias_vals_db[0].band_5
                bias_vals[5] = bias_vals_db[0].band_6
                bias_vals[6] = bias_vals_db[0].band_7
                bias_vals[7] = bias_vals_db[0].band_8
                bias_vals[8] = bias_vals_db[0].band_9
                bias_vals[9] = bias_vals_db[0].band_10
                bias_vals[10] = bias_vals_db[0].band_11
                bias_vals[11] = bias_vals_db[0].band_12
                bias_vals[12] = bias_vals_db[0].band_13

                bias_unc_vals[0] = bias_unc_vals_db[0].band_1
                bias_unc_vals[1] = bias_unc_vals_db[0].band_2
                bias_unc_vals[2] = bias_unc_vals_db[0].band_3
                bias_unc_vals[3] = bias_unc_vals_db[0].band_4
                bias_unc_vals[4] = bias_unc_vals_db[0].band_5
                bias_unc_vals[5] = bias_unc_vals_db[0].band_6
                bias_unc_vals[6] = bias_unc_vals_db[0].band_7
                bias_unc_vals[7] = bias_unc_vals_db[0].band_8
                bias_unc_vals[8] = bias_unc_vals_db[0].band_9
                bias_unc_vals[9] = bias_unc_vals_db[0].band_10
                bias_unc_vals[10] = bias_unc_vals_db[0].band_11
                bias_unc_vals[11] = bias_unc_vals_db[0].band_12
                bias_unc_vals[12] = bias_unc_vals_db[0].band_13

                meas_vals_sensor1[0] = meas_vals_sensor1_db.band_1
                meas_vals_sensor1[1] = meas_vals_sensor1_db.band_2
                meas_vals_sensor1[2] = meas_vals_sensor1_db.band_3
                meas_vals_sensor1[3] = meas_vals_sensor1_db.band_4
                meas_vals_sensor1[4] = meas_vals_sensor1_db.band_5
                meas_vals_sensor1[5] = meas_vals_sensor1_db.band_6
                meas_vals_sensor1[6] = meas_vals_sensor1_db.band_7
                meas_vals_sensor1[7] = meas_vals_sensor1_db.band_8
                meas_vals_sensor1[8] = meas_vals_sensor1_db.band_9
                meas_vals_sensor1[9] = meas_vals_sensor1_db.band_10
                meas_vals_sensor1[10] = meas_vals_sensor1_db.band_11
                meas_vals_sensor1[11] = meas_vals_sensor1_db.band_12
                meas_vals_sensor1[12] = meas_vals_sensor1_db.band_13

                meas_vals_sensor2[0] = meas_vals_sensor2_db.band_1
                meas_vals_sensor2[1] = meas_vals_sensor2_db.band_2
                meas_vals_sensor2[2] = meas_vals_sensor2_db.band_3
                meas_vals_sensor2[3] = meas_vals_sensor2_db.band_4
                meas_vals_sensor2[4] = meas_vals_sensor2_db.band_5
                meas_vals_sensor2[5] = meas_vals_sensor2_db.band_6
                meas_vals_sensor2[6] = meas_vals_sensor2_db.band_7
                meas_vals_sensor2[7] = meas_vals_sensor2_db.band_8
                meas_vals_sensor2[8] = meas_vals_sensor2_db.band_9
                meas_vals_sensor2[9] = meas_vals_sensor2_db.band_10
                meas_vals_sensor2[10] = meas_vals_sensor2_db.band_11
                meas_vals_sensor2[11] = meas_vals_sensor2_db.band_12
                meas_vals_sensor2[12] = meas_vals_sensor2_db.band_13

                # convert null vals back to nan - db tables do not accept nan values
                bias_vals[bias_vals == -9999] = np.nan
                bias_unc_vals[bias_unc_vals == -9999] = np.nan
                meas_vals_sensor1[meas_vals_sensor1 == -9999] = np.nan
                meas_vals_sensor2[meas_vals_sensor2 == -9999] = np.nan

                mup.sensor_1_wavelengths = [val for val in mup.sensor_1_wavelengths if val != '9999.0']

                # add in attrs and data_vars per matchup
                mup_info.attrs[sensor1 + '_' + ref + '_' + 'Datetime'][k] = mup.product_date
                mup_info[str(sensor1) + '_' + str(ref) + '_BiasVals'].values[k] = xr.DataArray(data=bias_vals.flatten())
                mup_info[str(sensor1) + '_' + str(ref) + '_BiasUncVals'].values[k] = xr.DataArray(data=bias_unc_vals.flatten())
                mup_info[str(sensor1) + '_' + str(ref) + '_MeasValsSensor1'].values[k] = xr.DataArray(data=meas_vals_sensor1.flatten())
                mup_info[str(sensor1) + '_' + str(ref) + '_MeasValsSensor2'].values[k] = xr.DataArray(data=meas_vals_sensor2.flatten())
                mup_info.attrs[str(sensor1) + '_' + str(ref) + '_Metadata'][str(mup.id)] = {
                    'Mission & Reference Site': sat_name[sensor1]+' & '+str(sensor2),
                    'Mission Date & Time': mup.product_date,
                    'Mission Satellite ID': mup.sensor1_id,
                    'Cloud Percentage': str(mup.sensor1_tile_cloud_percentage)+'%',
                    'Satellite Viewing Angle': str(round(mup.sensor1_view_angle, 2))+'°',
                    'Solar Azimuth Angle': str(round(mup.sensor1_sun_azimuth, 2))+'°',
                    'Solar Elevation Angle': str(round(mup.sensor1_sun_elevation, 2))+'°',
                    'AOD at 550 nm *': str(mup.AOD)+' nm',
                    # 'Mission Product': mup.full_sensor_1_prod_name,  # 'S2A_MSIL1C_20200327T110651_N0209_R137_T30UXC_20200327T115046'
                    # 'Reference Product': (ref + '_' + str(mup.product_date).split(' ')[0] + '_v04.09').replace('-', '_'),  # mup.full_sensor_2_prod_name, - need to add this in earlier in pipeline
                    # '...': np.nan
                }
                mup_ids.append(str(mup.id))

            # add in attrs per ref site
            mup_info.attrs[str(sensor1) + '_' + str(ref) + '_BandsSensor1'] = mup.sensor_1_bands
            mup_info.attrs[str(sensor1) + '_' + str(ref) + '_BandsSensor2'] = mup.sensor_2_bands
            mup_info.attrs[str(sensor1) + '_' + str(ref) + '_CentralWavelengthsSensor1'] = mup.sensor_1_wavelengths
            mup_info.attrs[str(sensor1) + '_' + str(ref) + '_MatchupIDs'] = mup_ids

    return mup_info


# return timeseries data for plotting, per ref site selected - currently only works for max 2 ref sites
def return_timeseries_data(sat, refs, band, dates):
    bands = natsorted(band)
    refs = sorted(refs)

    date_range = [datetime.strptime(dates[0],"%Y-%m-%d"),
                 datetime.strptime(dates[1],"%Y-%m-%d")
                 ]


    timeseries_data_all_bands = extract_mup_info_from_db(sat, refs, date_range)
    empty_df = pd.DataFrame(columns=['Datetime', 'BiasVals', 'BiasUncVals',
                                                 'MeasValsSensor1', 'MeasValsSensor2'])
    if not timeseries_data_all_bands.data_vars:
        return empty_df, empty_df

    if sat == 'planet':
        bands_idx = planet_bands_idx
    elif sat in ['s2', 's2a', 's2b',]:
        bands_idx = s2_bands_idx
    elif sat == 'l8':
        bands_idx = l8_bands_idx
    elif sat == 'airbus_phr':
        bands_idx = airbus_bands_idx

    clicked_band_idx = []
    for bnd in bands:
        clicked_band_idx.append(bands_idx[bnd])

    # return the timeseries data as df for plotting
    timeseries_data_ref1 = pd.DataFrame(index=range(timeseries_data_all_bands.data_vars[str(sat)+'_'+str(refs[0])+'_BiasVals'].values.shape[0]),
                                        columns=['Datetime', 'BiasVals', 'BiasUncVals',
                                                 'MeasValsSensor1', 'MeasValsSensor2']
                                        )

    for i in range(len(timeseries_data_ref1.index)):
        timeseries_data_ref1['Datetime'].iloc[i] = timeseries_data_all_bands.attrs[str(sat)+'_'+str(refs[0])+'_Datetime'][i]
        timeseries_data_ref1['BiasVals'].iloc[i] = timeseries_data_all_bands.data_vars[str(sat)+'_'+str(refs[0])+'_BiasVals'].values[i][[clicked_band_idx]]
        timeseries_data_ref1['BiasUncVals'].iloc[i] = timeseries_data_all_bands.data_vars[str(sat)+'_'+str(refs[0])+'_BiasUncVals'].values[i][[clicked_band_idx]]
        timeseries_data_ref1['MeasValsSensor1'].iloc[i] = timeseries_data_all_bands.data_vars[str(sat)+'_'+str(refs[0])+'_MeasValsSensor1'].values[i][[clicked_band_idx]]
        timeseries_data_ref1['MeasValsSensor2'].iloc[i] = timeseries_data_all_bands.data_vars[str(sat)+'_'+str(refs[0])+'_MeasValsSensor2'].values[i][[clicked_band_idx]]

    if len(refs) > 1:
        timeseries_data_ref2 = pd.DataFrame(index=range(timeseries_data_all_bands.data_vars[str(sat) + '_' + str(refs[1])+'_BiasVals'].values.shape[0]),
                                            columns=['Datetime', 'BiasVals', 'BiasUncVals',
                                                     'MeasValsSensor1', 'MeasValsSensor2']
                                            )

        for i in range(len(timeseries_data_ref2.index)):
            timeseries_data_ref2['Datetime'].iloc[i] = timeseries_data_all_bands.attrs[str(sat)+'_'+str(refs[1])+'_Datetime'][i]
            timeseries_data_ref2['BiasVals'].iloc[i] = timeseries_data_all_bands.data_vars[str(sat)+'_'+str(refs[1])+'_BiasVals'].values[i][[clicked_band_idx]]
            timeseries_data_ref2['BiasUncVals'].iloc[i] = timeseries_data_all_bands.data_vars[str(sat)+'_'+str(refs[1])+'_BiasUncVals'].values[i][[clicked_band_idx]]
            timeseries_data_ref2['MeasValsSensor1'].iloc[i] = timeseries_data_all_bands.data_vars[str(sat)+'_'+str(refs[1])+'_MeasValsSensor1'].values[i][[clicked_band_idx]]
            timeseries_data_ref2['MeasValsSensor2'].iloc[i] = timeseries_data_all_bands.data_vars[str(sat)+'_'+str(refs[1])+'_MeasValsSensor2'].values[i][[clicked_band_idx]]
    else:
        timeseries_data_ref2 = pd.DataFrame(index=range(timeseries_data_all_bands.data_vars[str(sat) + '_' + str(refs[0])+'_BiasVals'].values.shape[0]),
                                            columns=['Datetime', 'BiasVals', 'BiasUncVals',
                                                     'MeasValsSensor1', 'MeasValsSensor2']
                                            )
    return timeseries_data_ref1, timeseries_data_ref2


# plot upper plot timeseries data
def plot_timeseries(sat, band, refs, date_df_r1, bias_r1, bias_unc_r1, meas_vals_r1,
                    date_df_r2, bias_r2, bias_unc_r2, meas_vals_r2,
                    hyp_bias=None, hyp_bias_unc=None):

    bands = natsorted(band)
    refs = sorted(refs)

    bias_vals_r1 = np.ones((len(bands), len(date_df_r1)))*np.nan
    bias_unc_vals_r1 = np.ones((len(bands), len(date_df_r1)))*np.nan
    rcn_meas_vals_r1 = np.ones((len(bands), len(date_df_r1)))*np.nan
    bias_vals_r2 = np.ones((len(bands), len(date_df_r2))) * np.nan
    bias_unc_vals_r2 = np.ones((len(bands), len(date_df_r2))) * np.nan
    rcn_meas_vals_r2 = np.ones((len(bands), len(date_df_r2))) * np.nan

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

    bias_percentage_r1 = np.ones(bias_vals_r1.shape)*np.nan
    bias_percentage_r2 = np.ones(bias_vals_r2.shape)*np.nan

    # calculate bias percentage
    for k in range(len(bands)):
        bias_percentage_r1[k] = bias_vals_r1[k] / rcn_meas_vals_r1[k] * 100
        bias_percentage_r2[k] = bias_vals_r2[k] / rcn_meas_vals_r2[k] * 100

    timeseries_fig = go.Figure()

    for i in range(len(bands)):
        timeseries_fig.add_trace(
            go.Scatter(x=date_df_r1, y=bias_percentage_r1[i], mode='lines+markers',
                       name=bands[i],
                       error_y_array=bias_unc_vals_r1[i],
                       legendgroup='group1', legendgrouptitle_text=f'{refs[0]}'))
        if len(refs) >1:
            timeseries_fig.add_trace(
                go.Scatter(x=date_df_r2, y=bias_percentage_r2[i], mode='lines+markers',
                           name=bands[i],
                           error_y_array=bias_unc_vals_r2[i],
                           legendgroup='group2', legendgrouptitle_text=f'{refs[-1]}'))

    timeseries_fig.update_traces(
        line=dict(dash='dash', width=0),
        marker=dict(size=10, symbol='hexagon'),
        showlegend=True
    )
    timeseries_fig.update_layout(
        clickmode='event+select',
        # title={
        #     'text': f"{rcn_site} and {hyp_site} Sites Compared with {sat}",
        #     'x': 0.5,
        #     'xanchor': 'center',
        #     'yanchor': 'top'},
        legend_title_text=sat_name[str(sat)]+'<br>Wavelengths',
        legend=dict(groupclick="toggleitem"),  # "togglegroup"
    )
    timeseries_fig.layout.margin = {'t': 10,
                           'b': 10,
                           'r': 0,
                           'l': 20}
    timeseries_fig.update_yaxes(
        title={'text': 'Percentage Difference', 'font.size': 15},
        tickfont_size=15,
        griddash='solid',
        gridwidth=2,
        linewidth=2,
        linecolor='navy',
        minor={
            'griddash': 'solid',
            'nticks': 5,
            'gridcolor': 'white',  # aquamarine #aliceblue
            'gridwidth': 0.5})
    timeseries_fig.update_xaxes(
        # tickangle=90,
        title={'text': 'Date', 'font.size': 15},
        tickfont_size=15,
        linewidth=2,
        linecolor='navy')

    return timeseries_fig


# populate upper panel table with mean bias vals
def get_bias_table_vals(sat, refs, bands, date_df_r1, bias_r1, bias_unc_r1, meas_vals_r1,
                    date_df_r2=None, bias_r2=None, bias_unc_r2=None, meas_vals_r2=None):
    bias_vals = {}
    band = natsorted(bands)
    refs = sorted(refs)

    if date_df_r2.empty:
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
        bias_vals_mean_r1.append(round(sum(bias_percentage_r1[k][~np.isnan(bias_percentage_r1[k])]) / len(bias_percentage_r1[k][~np.isnan(bias_percentage_r1[k])]), 2))
        if len(refs) > 1:
            bias_vals_mean_r2.append(round(sum(bias_percentage_r2[k][~np.isnan(bias_percentage_r2[k])]) / len(bias_percentage_r2[k][~np.isnan(bias_percentage_r2[k])]), 2))

    # find relevant bands and order based on sat
    for ref in refs:
        if ref == refs[0]:
            rcn_bias_vals_mean = bias_vals_mean_r1
        else:
            rcn_bias_vals_mean = bias_vals_mean_r2
        for k in range(len(band)):
            if sat == 'planet':
                    bias_vals[ref+' B' + str(planet_bands_idx[band[k]] + 1) + ' - ' + str(band[k])] = f'{rcn_bias_vals_mean[k]}%'
            elif sat == 'airbus_phr':
                bias_vals[ref+' B' + str(airbus_bands_idx[band[k]] + 1) + ' - ' + str(band[k])] = f'{rcn_bias_vals_mean[k]}%'
            elif sat == 'l8':
                bias_vals[ref+' B' + str(l8_bands_idx[band[k]] + 1) + ' - ' + str(band[k])] = f'{rcn_bias_vals_mean[k]}%'
            elif sat in ['s2a', 's2b', 's2']:
                if s2_bands_idx[band[k]] <= 7:
                    bias_vals[ref+' B' + str(s2_bands_idx[band[k]] + 1) + ' - ' + str(band[k])] = f'{rcn_bias_vals_mean[k]}%'
                elif s2_bands_idx[band[k]] == 8:
                    bias_vals[ref+' B8A' + ' - ' + str(band[k])] = f'{rcn_bias_vals_mean[k]}%'
                else:
                    bias_vals[ref+' B' + str(s2_bands_idx[band[k]]) + ' - ' + str(band[k])] = f'{rcn_bias_vals_mean[k]}%'

    bias_vals_sorted = dict(natsorted(bias_vals.items()))

    for k, v in bias_vals_sorted.items():
        if v == '-0.0%':
            bias_vals_sorted[k] = '0.0%'

    return bias_vals_sorted


# populate matchup analysis table
def analysis_table_update(sat, refs, mup_info):

    col_1 = []
    col_2 = []

    # extract metadata for analysis table and convert to correct format for input
    for key in mup_info.attrs[f'{sat}_{refs[0]}_Metadata'].keys():
        mup_id = key
    for k, v in mup_info.attrs[f'{sat}_{refs[0]}_Metadata'][mup_id].items():
        col_1.append(k)
        col_2.append(v)

    for i, val in enumerate(col_2):
        if isinstance(val, datetime):
            col_2[i] = val.strftime('%Y-%m-%d %H:%M:%S')

    matchup_analysis_df = pd.DataFrame(data={'column_1': col_1,
                                             'column_2': col_2,
                                             },
                                       index=range(len(col_1))
                                       )

    matchup_analysis_df['column_2'][0] = sat_name[sat]+' & '+ref_name[refs[0]].split('-')[0][:-1]+ref_name[refs[0]].split('-')[1]

    matchup_analysis =  matchup_analysis_df.to_dict('records'), [{"name": i, "id": i} for i in matchup_analysis_df.columns]

    return matchup_analysis


# make small plot for bottom panel
def small_plot_update(sat, refs, mup_info):

    ref = refs[0]

    # reorder indices so that for S-2 B8A (with corresponding data) slots in between B8-B9
    sensor_1_meas_vals = mup_info.data_vars[f'{sat}_{ref}_MeasValsSensor1'].values.flatten()
    sensor_2_meas_vals = mup_info.data_vars[f'{sat}_{ref}_MeasValsSensor2'].values.flatten()
    sensor_1_wav_vals = mup_info.attrs[f'{sat}_{ref}_CentralWavelengthsSensor1']

    # if s2 - show only 5 bands
    if sat == 's2':
        sensor_1_meas_vals = sensor_1_meas_vals[0:5]
        sensor_2_meas_vals = sensor_2_meas_vals[0:5]

    sensor_1_wav_sort = sensor_1_wav_vals

    for i, val in enumerate(sensor_1_wav_sort):
        sensor_1_wav_sort[i] = val.split('.')[0]

    fig_small = go.Figure()
    fig_small.add_trace(
        go.Scatter(x=sensor_1_wav_sort, y=sensor_1_meas_vals, mode='lines+markers',
                   name=sat_name[sat],
                   ))
    # line_color=color_group[i],
    # marker_color=color_group[i]))
    fig_small.add_trace(
        go.Scatter(x=sensor_1_wav_sort, y=sensor_2_meas_vals, mode='lines+markers',
                   name=ref_name[ref],
                   ))
    fig_small.update_traces(line=dict(dash='dash', width=2),
                            marker=dict(size=10),
                            showlegend=True
                            )
    fig_small.update_layout(
        legend=dict(x=0, y=1, xanchor='left', yanchor='top', bgcolor='rgba(0,0,0,0)'),
    )
    fig_small.layout.margin = {'t': 10,
                               'b': 10,
                               'r': 0,
                               'l': 20}
    fig_small.update_yaxes(
        title={'text': 'Reflectance', 'font.size': 15},
        tickfont_size=15,
        linewidth=2,
        linecolor='navy',
        minor={
            'griddash': 'solid',
            'nticks': 5,
            'gridcolor': 'white',  # aquamarine #aliceblue
            'gridwidth': 0.5})
    fig_small.update_xaxes(
        tickangle=60,
        title={'text': 'Wavelength', 'font.size': 15},
        tickfont_size=15,
        linewidth=2,
        linecolor='navy')

    return fig_small


if __name__ == '__main__':
    pass
