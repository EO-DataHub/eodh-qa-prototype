import dash
from dash import html, dcc, callback, Output, Input, dash_table, State
import dash_bootstrap_components as dbc
import datetime
import dash_mantine_components as dmc
import plotly.graph_objects as go
import pandas as pd
import flask
import urllib
import os
import sys

# to find data_interface within docker container
data_dir = os.path.join('\\'.join(os.getcwd().split('\\')[:-1]))
sys.path.insert(1, data_dir)
import data_interface

dash.register_page(__name__,
                   order=2,
                   title='Calibration Dashboard',  # name of tab
                   name = 'Dashboard',
                   # image='dashboard.png',
                   description='CEOS Calibration Dashboard.',
                   location="sidebar",
                   # redirect_from='/home'
                   )

HEIGHT_OF_ROW = 345

# create empty graph placeholder for plots
fig_empty = go.Figure()
fig_empty.layout.margin = {'t': 10,
                           'b': 10,
                           'r': 0,
                           'l': 20}

lower_dummy_plot = dcc.Graph(figure=fig_empty,
                             id='lower-dummy-plot-content',
                             style={'height': '40vh', 'width': '60vh'}
                             )

# get loading spinner for upper plot
upper_plot = dbc.Spinner(
    dcc.Graph(figure=fig_empty, id='upper-graph-content',
                        style={'height': '55vh', 'width': '120vh'},
                        ),
    color="primary",
    spinner_style={"width": "3rem", "height": "3rem"}
)

# create control panel in upper container - select mission, reference site, bands, date range
control_panel = dmc.Card(
    # style={'height': '65vh',
    #        # 'width': '60vh' # CHANGED
    #        },
    withBorder=True,
    shadow="xs",
    radius="md",
    children=[
        dmc.Container(fluid=True, style={'margin-bottom': '124px'}, children=[
            dbc.Row(
                dbc.Col(children=[
                    dmc.Text("Mission:", weight=500, style={'margin-top': '10px', 'padding-bottom': '5px'}),
                    # 'padding-left': '5px'
                    dcc.Dropdown(
                        id='sat',
                        placeholder="Select a mission...",
                        clearable=True,
                        multi=False,
                        # style={'padding-left': '10px', 'padding-bottom': '5px'},
                        # value=out_platform_type,
                        options=[
                            {'label': 'Sentinel-2A', 'value': 's2a'},
                            {'label': 'Sentinel-2B', 'value': 's2b'},
                            {'label': 'Landsat 8', 'value': 'l8'},
                            {'label': 'Planet SuperDove', 'value': 'planet'},
                            {'label': 'Airbus Pleiades', 'value': 'airbus_phr'},
                        ]
                    )])),
            dbc.Row(
                dbc.Col(children=[
                    dmc.Text("Reference:",
                             weight=500,
                             style={'margin-top': '20px', 'padding-bottom': '5px'}),
                    # 'padding-left': '5px',
                    dcc.Dropdown(
                        id='ref',
                        placeholder="Select a reference...",
                        clearable=True,
                        multi=True,
                        # style={'padding-left': '10px'},
                        # value=out_platform_type,
                        options=[
                            {'label': 'RadCalNet - GONA', 'value': 'RCN-GONA'},
                            {'label': 'RadCalNet - RVUS', 'value': 'RCN-RVUS'},
                            {'label': 'HYPERNETS - GHNA', 'value': 'HYP-GHNA'}
                        ]
                    )])),
            dbc.Row(
                dbc.Col(children=[
                    dmc.Text("Wavebands:", weight=500,  # id='band_text',
                             style={'margin-top': '20px', 'padding-bottom': '5px', 'padding-left': '5px'}),
                    dcc.Dropdown(
                        id='band',
                        placeholder="Select wavebands...",
                        clearable=True,
                        multi=True,
                        # style={'padding-left': '10px'},
                        options=[]
                    )])),
            dbc.Row(
                dbc.Col(children=[
                    dmc.Text("Date range:", weight=500, style={'margin-top': '20px',
                                                               # 'padding-left': '5px',
                                                               'padding-bottom': '5px'}),
                    dmc.DateRangePicker(
                        id="date-picker",
                        # label="Start Date",
                        # description="description",
                        inputFormat="DD-MM-YYYY",
                        minDate=datetime.date(2010, 1, 1),
                        value=[datetime.date(2022, 1, 1), datetime.date(2022, 12, 30)],
                        style={'font-size': '0.2rem'},
                        # display='',
                        # dropdownPosition='up',
                        dropdownType='',  # makes datepicker a popup box
                        placeholder='DD-MM-YYYY'
                    )
                ]))
        ]
                      )],
)

# average biases table empty data
av_bias_dict_empty = {'': '', ' ': '', '  ': '', '   ': '', '    ': '', '     ': ''}
matchup_analysis_dict_empty = {'': ('Mission & Reference Site', 'Mission Time', 'Mission Satellite ID', 'Cloud Percentage', 'Satellite Viewing Angle', 'Sun Azimuth Angle', 'AOD at 550 nm *',
                                    # 'Mission Product', 'Reference Product'
                                    ),
                               ' ': ('', '', '', '', '', '', '', #'', ''
                                     )}

av_bias_empty = pd.DataFrame(data=av_bias_dict_empty, index=[0])
matchup_analysis_empty = pd.DataFrame(data=matchup_analysis_dict_empty)

# create upper panel containing timeseries plot and average bias table
upper_plot_panel = dmc.Card(
    # style={'height': '65vh', 'width': '120vh'},
    withBorder=True, shadow="xs", radius="md",
    children=[dbc.Row(dcc.Markdown('''
            **Comparison Time Series**
            ''')),
              dbc.Row(upper_plot, style={'margin-bottom': '10px'}),
              dcc.Markdown("Mean bias: "),
              dbc.Row(dbc.Container(style={'margin-left': '15px', 'width': '115vh'}, fluid='xs', children=[
                  dash_table.DataTable(av_bias_empty.to_dict('records'),
                                       [{"name": i, "id": i} for i in av_bias_empty.columns],
                                       id='average_bias_tbl-content',
                                       # fill_width=True,
                                       style_cell={'padding': '5px', 'textAlign': 'left',
                                                   'whiteSpace': 'pre-line', 'height': 'auto',
                                                   'maxWidth': '20px',
                                                   # 'font-size': '0.8rem'
                                                   },
                                       style_header={
                                           'backgroundColor': 'rgb(220, 230, 250)',
                                           'fontWeight': 'bold',
                                           'font-size': '0.8rem',
                                           'font-family': 'Helvetica',
                                           'whiteSpace': 'normal',
                                           'height': 'auto'},
                                       style_data={
                                           'color': 'black',
                                           'backgroundColor': 'white',
                                           'whiteSpace': 'normal', 'height': 'auto',
                                           'font-size': '0.9rem',
                                       },
                                       fixed_rows={'headers': True, 'data': 0},
                                       css=[{
                                           'selector': '.dash-spreadsheet td div',
                                           'rule': '''
                                                      line-height: 18px; max-height: 18px; min-height: 18px; height: 18px;
                                                      display: inline-block;
                                                      word-wrap: break-word;
                                                      text-overflow: inherit;
                                                      '''
                                       }]
                                       )
              ]))
              ]
)

# combine control and upper plot panels into one row
top_panels = dmc.Container(fluid=True, children=[
    dbc.Row(children=[
        dbc.Col(control_panel),  # xs=2, sm=2, md=2, lg=2,
        dbc.Col(
            children=[
            upper_plot_panel
    ]
        ,  # xs=2, sm=2, md=2, lg=2,
                style={'margin-left': '10px'},
                )
    ])
])

# create bottom panel for matchup analysis table, picture of reference site location and small comparison data plot
bottom_panel = dmc.Card(
    # style={'margin-bottom': '10px', 'margin-top': '10px'},
    withBorder=True, shadow="xs", radius="md",
    children=[
        dbc.Container(fluid=True, children=[
            dbc.Row(dbc.Col(dcc.Markdown('''
            **Matchup Analysis**
            '''))),
            dbc.Row(children=[
                dbc.Col(style={'margin-left': '2vh'},
                        children=[dbc.Container(fluid='xs', children=[
                            dash_table.DataTable(matchup_analysis_empty.to_dict('records'),
                                                 [{"name": i, "id": i} for i in matchup_analysis_empty.columns],
                                                 id='matchup_analysis_tbl-content',
                                                 fill_width=True,
                                                 style_cell={'padding': '5px', 'textAlign': 'left',
                                                             'whiteSpace': 'pre-line', 'height': 'auto',
                                                             'maxWidth': '20vh'},
                                                 style_header={
                                                     'display': 'none'},
                                                 style_data={
                                                     'color': 'black',
                                                     'backgroundColor': 'white',
                                                     'whiteSpace': 'normal', 'height': 'auto'},
                                                 # wraps text within cells
                                                 style_data_conditional=[{
                                                     'if': {'row_index': 0},
                                                     'backgroundColor': 'rgb(220, 230, 250)'},
                                                     # {'if': {'row_index': 'odd'},
                                                     #     'backgroundColor': 'rgb(220, 230, 250)'}
                                                 ],
                                                 fixed_rows={'headers': False, 'data': 0},
                                                 css=[{
                                                     'selector': '.dash-spreadsheet td div',
                                                     'rule': '''
                                                                line-height: 15px; max-height: 32px; min-height: 32px; height: 32px;
                                                                display: inline-block;
                                                                word-wrap: break-word;
                                                                text-overflow: inherit;
                                                                '''
                                                 }]  # overflow-y: visible; overflow-x: visible;
                                                 ),

                        ])]),
                dbc.Col(
                    style={'margin-left': '4vh'},  # 'width': '450px',
                    children=[dbc.Container(fluid='xs', children=[
                        dbc.CardBody(
                            dcc.Markdown("Scene Location")), # Site Map /
                        html.Img(id='quicklook-image-content',
                                 src='assets/empty_quicklook.png',
                                 style={'width': '50vh'})
                    ])]),

                dbc.Col(
                    style={'margin-left': '-10vh'},
                        #'width': '500px', 'margin-right': '10px'},
                    children=[dbc.Container(fluid=True, children=[
                        dcc.Markdown("Comparison Data"),
                        lower_dummy_plot,
                    ])])
            ]),
            dbc.Row(
                dbc.Col(dcc.Markdown(''' _\* All information is from satellite product metadata, \
            except AOD which is from the RadCalNet reference site metadata._
            '''), style={'padding-top': '15px'})),
            ])])


layout = html.Div(children=[
    dcc.Location(id='url', refresh=False,), # pathname='ceos_dashboard'),
    dcc.Interval(id='trigger', n_intervals=0,
                     max_intervals=0,  #<-- only run once
                     interval=1),
    dbc.Row(

        dbc.Col(top_panels,
                style={'margin-top': '0vh',
                       'margin-left': '75px', 'margin-right': '75px'})

    ),
    dbc.Row(
        [
            dbc.Col(bottom_panel,
                    style={'margin-top': '5vh', 'margin-bottom': '5vh',
                           'margin-left': '75px', 'margin-right': '75px'}, )
            # xs=12, sm=12, md=12, lg=12)
        ]
    ),
])

# band options for Sentinel-2 (using same for S2A and S2B within control panel bands selection), Landsat 8, Planet SuperDove, Airbus Pleiades
options_s2 = [
    {'label': 'B1 - 442 nm', 'value': '442 nm'},
    {'label': 'B2 - 492 nm', 'value': '492 nm'},
    {'label': 'B3 - 559 nm', 'value': '559 nm'},
    {'label': 'B4 - 664 nm', 'value': '664 nm'},
    {'label': 'B5 - 704 nm', 'value': '704 nm'},
    {'label': 'B6 - 740 nm', 'value': '740 nm'},
    {'label': 'B7 - 782 nm', 'value': '782 nm'},
    {'label': 'B8 - 832 nm', 'value': '832 nm'},
    {'label': 'B8A - 864 nm', 'value': '864 nm'},
    {'label': 'B9 - 945 nm', 'value': '945 nm'},
    {'label': 'B10 - 1373 nm', 'value': '1373 nm'},
    {'label': 'B11 - 1613 nm', 'value': '1613 nm'},
]

# options_s2a = [ # diferente for S2B?
#     {'label': 'B1 - 443 nm', 'value': '443 nm'},
#     {'label': 'B2 - 492 nm', 'value': '492 nm'},
#     {'label': 'B3 - 560 nm', 'value': '560 nm'},
#     {'label': 'B4 - 665 nm', 'value': '665 nm'},
#     {'label': 'B5 - 704 nm', 'value': '704 nm'},
#     {'label': 'B6 - 741 nm', 'value': '741 nm'},
#     {'label': 'B7 - 783 nm', 'value': '783 nm'},
#     {'label': 'B8 - 833 nm', 'value': '833 nm'},
#     {'label': 'B8A - 865 nm', 'value': '865 nm'},
#     {'label': 'B9 - 945 nm', 'value': '945 nm'},
#     {'label': 'B10 - 1374 nm', 'value': '1374 nm'},
#     {'label': 'B11 - 1614 nm', 'value': '1614 nm'},
#     {'label': 'B12 - 2202 nm', 'value': '2202 nm'}
# ]

# options_s2b = [
#     {'label': 'B1 - 442 nm', 'value': '442 nm'},
#     {'label': 'B2 - 492 nm', 'value': '492 nm'},
#     {'label': 'B3 - 559 nm', 'value': '559 nm'},
#     {'label': 'B4 - 665 nm', 'value': '665 nm'},
#     {'label': 'B5 - 704 nm', 'value': '704 nm'},
#     {'label': 'B6 - 739 nm', 'value': '739 nm'},
#     {'label': 'B7 - 780 nm', 'value': '780 nm'},
#     {'label': 'B8 - 833 nm', 'value': '833 nm'},
#     {'label': 'B8A - 864 nm', 'value': '864 nm'},
#     {'label': 'B9 - 943 nm', 'value': '943 nm'},
#     {'label': 'B10 - 1377 nm', 'value': '1377 nm'},
#     {'label': 'B11 - 1610 nm', 'value': '1610 nm'},
#     {'label': 'B12 - 2186 nm', 'value': '2186 nm'}
# ]

options_l8 = [
    {'label': 'B1 - 443 nm', 'value': '443'},
    {'label': 'B2 - 483 nm', 'value': '483'},
    {'label': 'B3 - 560 nm', 'value': '560'},
    {'label': 'B4 - 660 nm', 'value': '660'},
    {'label': 'B5 - 865 nm', 'value': '865'},
    {'label': 'B6 - 1650 nm', 'value': '1650'},
    {'label': 'B7 - 2220 nm', 'value': '2220'},
    {'label': 'B8 - 640 nm', 'value': '640'},
    {'label': 'B9 - 1375 nm', 'value': '1375'},
]

options_planet = [
    {'label': 'B1 - 442 nm', 'value': '442 nm'},
    {'label': 'B2 - 490 nm', 'value': '490 nm'},
    {'label': 'B3 - 531 nm', 'value': '531 nm'},
    {'label': 'B4 - 565 nm', 'value': '565 nm'},
    {'label': 'B5 - 610 nm', 'value': '610 nm'},
    {'label': 'B6 - 665 nm', 'value': '665 nm'},
    {'label': 'B7 - 705 nm', 'value': '705 nm'},
    {'label': 'B8 - 865 nm', 'value': '865 nm'},
]

options_airbus = [
    {'label': 'B1 - 490 nm', 'value': '490 nm'},
    {'label': 'B2 - 560 nm', 'value': '560 nm'},
    {'label': 'B3 - 650 nm', 'value': '650 nm'},
    {'label': 'B4 - 840 nm', 'value': '840 nm'},
]

all_options = pd.DataFrame(data=[options_s2, options_l8, options_planet, options_airbus], index=['s2', 'l8', 'planet', 'airbus_phr'])  # 's2a', 's2b',

all_options_dict = {'s2': options_s2, 's2a': options_s2, 's2b': options_s2, 'l8': options_l8,
                    'planet': options_planet, 'airbus_phr': options_airbus}


# updates control panel wavebands based on satellite selection
@callback(
    Output('band', 'options', allow_duplicate=True),
    Input('sat', 'value'),
    prevent_initial_call=True,
)
def update_band_selector(selected_sat):
    if selected_sat is None:
        return []
    return [{'label': band_i['label'], 'value': band_i['value']} for band_i in all_options_dict[selected_sat]]


# updates the upper panel timeseries plot based on control panel selection
@callback(
    Output('upper-graph-content', 'figure'),
    # Input('dropdown-selection', 'value')
    Input('sat', 'value'),
    Input('ref', 'value'),
    Input('band', 'value'),
    Input('date-picker', 'value'),
    prevent_initial_call=True,
)
def update_timeseries(sat: list, refs: list, band: list, date: list):
    empty_upper_plot = fig_empty

    if any(val is None for val in [sat, refs, band, date]):
        return empty_upper_plot

    else:
        refs = sorted(refs)

        timeseries_data_ref1, timeseries_data_ref2 = data_interface.return_timeseries_data(sat, refs, band, date) # 2 pd dfs
        if len(timeseries_data_ref1) == 0 and len(timeseries_data_ref2) == 0:
            return empty_upper_plot

        upper_plot = data_interface.plot_timeseries(sat,
                                                    band,
                                                    refs,
                                                    timeseries_data_ref1['Datetime'],
                                                    timeseries_data_ref1['BiasVals'],
                                                    timeseries_data_ref1['BiasUncVals'],
                                                    timeseries_data_ref1['MeasValsSensor2'],
                                                    timeseries_data_ref2['Datetime'],
                                                    timeseries_data_ref2['BiasVals'],
                                                    timeseries_data_ref2['BiasUncVals'],
                                                    timeseries_data_ref2['MeasValsSensor2']
                                                    )

    return upper_plot


# updates top panel average bias table
@callback(
    Output('average_bias_tbl-content', 'data'),
    Output('average_bias_tbl-content', 'columns'),
    # Input('dropdown-selection', 'value')
    Input('sat', 'value'),
    Input('ref', 'value'),
    Input('band', 'value'),
    Input('date-picker', 'value'),
    prevent_initial_call=True
)
def update_bias_table(sat, refs, band, date):

    empty_bias_vals_table_output = (av_bias_empty.to_dict('records'),
                              [{"name": i, "id": i} for i in av_bias_empty.columns])

    if any(val is None for val in [sat, refs, band, date]):
        return empty_bias_vals_table_output

    else:
        ref = sorted(refs)

        timeseries_data_ref1, timeseries_data_ref2 = data_interface.return_timeseries_data(sat, ref, band, date)
        if len(timeseries_data_ref1) == 0 and len(timeseries_data_ref2) == 0:
            return empty_bias_vals_table_output

        else:
            bias_vals = data_interface.get_bias_table_vals(sat,
                                                           ref,
                                                           band,
                                                           timeseries_data_ref1['Datetime'],
                                                           timeseries_data_ref1['BiasVals'],
                                                           timeseries_data_ref1['BiasUncVals'],
                                                           timeseries_data_ref1['MeasValsSensor2'],
                                                           timeseries_data_ref2['Datetime'],
                                                           timeseries_data_ref2['BiasVals'],
                                                           timeseries_data_ref2['BiasUncVals'],
                                                           timeseries_data_ref2['MeasValsSensor2'],
                                                           )
            bias_vals_df = pd.DataFrame(data=bias_vals, index=[0])
            bias_vals_table_output = bias_vals_df.to_dict('records'), [{"name": i, "id": i} for i in bias_vals_df.columns]

    return bias_vals_table_output


# updates bottom panel parts
@callback(
    Output('lower-dummy-plot-content', 'figure'),
    Output('matchup_analysis_tbl-content', 'data'),
    Output('matchup_analysis_tbl-content', 'columns'),
    Output('quicklook-image-content', 'src'),
    Input('upper-graph-content', 'clickData'),
    Input('sat', 'value'),
    Input('ref', 'value'),
    prevent_initial_call=True
)
def update_bottom_panel(clickData, sat, refs): #band

    if any(val is None for val in [clickData, sat, refs]):
        output = fig_empty, matchup_analysis_empty.to_dict('records'), [{"name": i, "id": i} for i in matchup_analysis_empty.columns], 'assets/empty_quicklook.png'
    else:
        refs = sorted(refs)

        if len(refs) >= 2:
            if clickData['points'][0]['curveNumber'] in [0, 2, 4, 6, 8, 10, 12, 14]:  # only works for 2 refs for now
                clicked_ref = [refs[0]]
            else:
                clicked_ref = [refs[1]]
        else:
            clicked_ref = refs

        matchup_datetime = str(clickData['points'][0]['x']).split('.')[0]

        # convert dates into comparable format
        clicked_matchup_date = datetime.datetime.strptime(matchup_datetime, "%Y-%m-%d %H:%M:%S")

        matchup_range_end = clicked_matchup_date + datetime.timedelta(minutes=60)
        mup_info = data_interface.extract_mup_info_from_db(sat, clicked_ref, [clicked_matchup_date, matchup_range_end])

        data, columns = data_interface.analysis_table_update(sat, clicked_ref, mup_info)

        figure = data_interface.small_plot_update(sat, clicked_ref, mup_info)

        if clicked_ref == ['RCN-GONA']:  # currently works only for GONA and RVUS - update to get any ref based on clickData
            src = 'assets/Gobabeb.png'
        else:
            src = 'assets/RailroadValley.png'

        output = figure, data, columns, src

    return output


# runs on-load - builds the control panel and sets the options and values based on the state of the url
@callback(
    Output('sat', 'value'),
    Output('band', 'options'),
    Output('ref', 'value'),
    Output('band', 'value'),
    Output('date-picker', 'value'),
    Input('trigger', 'n_intervals'),
)
def read_url(trigger):
    out_sat = None
    out_refs = None
    out_bands = None
    out_date = None

    url = flask.request.referrer
    parts = urllib.parse.urlparse(url)
    params = urllib.parse.parse_qs(parts.query)

    if 'sat' in params:
        out_sat = params['sat'][0]

    if 'refs' in params:
        out_refs = []
        for i in range(len(params['refs'][0].split(','))):
            out_refs.append(params['refs'][0].split(',')[i])

    if 'bands' in params:
        out_bands = []
        for i in range(len(params['bands'][0].split(','))):
            out_bands.append(params['bands'][0].split(',')[i]+' nm')

    if 'date' in params:
        out_date = [params['date'][0].split(',')[0],params['date'][0].split(',')[1]]

    if out_sat is None:
        band_options = []
    else:
        band_options = [{'label': band_i['label'], 'value': band_i['value']} for band_i in all_options_dict[out_sat]]

    return out_sat, band_options, out_refs, out_bands, out_date

# updates url based on control panel selection
@callback(
        Output("url", "search"),
        Input('sat', 'value'),
        Input('ref', 'value'),
        Input('band', 'value'),
        Input('date-picker', 'value'),
    prevent_initial_call=True
    )
def display_page(sat, ref, band, date):
    vals = [sat, ref, band, date]
    vars = ['sat', 'refs', 'bands', 'date']

    search_output = '?'
    for i, val in enumerate(vals):
        if val is not None:
            if i == 0:  # sat
                search_output += f'{vars[i]}={val}&'
            elif i == 1:  # refs
                url_refs = ''
                for k in val:
                    url_refs += f'{k},'
                url_refs = url_refs[:-1]
                search_output += f'{vars[i]}={url_refs}&'
            elif i == 2:  # bands
                url_bands = ''
                for k in val:
                    url_bands += f'{k[:-3]},'
                url_bands = url_bands[:-1]
                search_output += f'{vars[i]}={url_bands}&'
            elif i == 3:  # dates
                url_dates = ''
                for k in val:
                    url_dates += f'{k},'
                url_dates = url_dates[:-1]
                search_output += f'{vars[i]}={url_dates}&'

    search_output = search_output[:-1]

    return search_output
