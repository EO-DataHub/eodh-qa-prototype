import dash
from dash import html, dcc, callback, Output, Input, dash_table, State
import dash_bootstrap_components as dbc
import datetime
import dash_mantine_components as dmc
import plotly.graph_objects as go
import pandas as pd
import flask
import urllib
from urllib.request import urlopen
import os
import sys

# to ensure paths are found correctly within Docker container for importing data_interface
data_dir = os.path.join("\\".join(__file__.split("\\")[:-2]))
sys.path.insert(1, data_dir)

import data_interface

dash.register_page(
    __name__,
    order=2,
    title="RadVAL Dashboard",  # name of tab
    name="RadVAL Dashboard",
    description="CEOS RadVAL Dashboard.",  # metadata
    location="sidebar",
    suppress_callback_exceptions=True,
)

HEIGHT_OF_ROW = 345

# create empty graph placeholder for plots
fig_empty = go.Figure()
fig_empty.layout.margin = {"t": 10, "b": 10, "r": 0, "l": 20}

graph_upper = dcc.Loading(
    [
        dcc.Graph(
            figure=fig_empty,
            id="upper-graph-content",
            # style={"height": "55vh", "width": "120vh"},
        )
    ],
    type="circle",
    color="red",
)

graph_dummy_small = dcc.Graph(
    figure=fig_empty,
    id="small-dummy-graph-content",
    style={"height": "40vh", "width": "60vh"},
)

# create control panel in upper container - select mission, reference site, bands, date range
control_panel = dmc.Card(
    style={"width": "350px"},
    withBorder=True,
    shadow="xs",
    radius="md",
    children=[
        dmc.Container(
            fluid=True,
            # style={"margin-bottom": "124px"},
            children=[
                dbc.Row(
                    dbc.Col(
                        children=[
                            dmc.Text(
                                "Mission:",
                                # weight=500,
                                style={
                                    "margin-top": "10px",
                                    "margin-bottom": "5px",
                                    #    "padding-bottom": "5px"
                                },
                            ),
                            # 'padding-left': '5px'
                            dcc.Dropdown(
                                id="sat",
                                placeholder="Select a mission...",
                                clearable=True,
                                multi=False,
                                # style={"width": "150px"},
                                # value=out_platform_type,
                                options=[
                                    {"label": "Sentinel-2A", "value": "s2a"},
                                    {"label": "Sentinel-2B", "value": "s2b"},
                                    {"label": "Landsat 8", "value": "l8"},
                                    {"label": "Landsat 9", "value": "l9"},
                                    {
                                        "label": "Planet SuperDove",
                                        "value": "planetscope",
                                    },
                                    {"label": "Airbus Pleiades", "value": "airbus_phr"},
                                ],
                            ),
                        ]
                    )
                ),
                dbc.Row(
                    dbc.Col(
                        children=[
                            dmc.Text(
                                "Reference:",
                                # weight=500,
                                style={
                                    "margin-top": "20px",
                                    "margin-bottom": "5px",
                                    #    "padding-bottom": "5px"
                                },
                            ),
                            # 'padding-left': '5px',
                            dcc.Dropdown(
                                id="ref",
                                placeholder="Select a reference...",
                                clearable=True,
                                multi=True,
                                # style={"width": "50px"},
                                # value=out_platform_type,
                                options=[
                                    {"label": "RadCalNet - GONA", "value": "RCN-GONA"},
                                    {"label": "RadCalNet - RVUS", "value": "RCN-RVUS"},
                                    {"label": "PICS - Libya 4", "value": "LIBYA-4"},
                                    {
                                        "label": "CEOS Virtual Reference",
                                        "value": "ceos-virtual-ref",
                                    },
                                    {
                                        "label": "PICS - Libya 1",
                                        "value": "LIBYA-1",
                                        "disabled": "True",
                                    },
                                    {
                                        "label": "PICS - Algeria 3",
                                        "value": "ALGERIA-3",
                                        "disabled": "True",
                                    },
                                    {
                                        "label": "PICS - Lake Tahoe",
                                        "value": "LAKE-TAHOE",
                                        "disabled": "True",
                                    },
                                ],
                            ),
                        ]
                    )
                ),
                dbc.Row(
                    dbc.Col(
                        children=[
                            dmc.Text(
                                "Wavebands:",  # weight=500,  # id='band_text',
                                style={
                                    "margin-top": "20px",
                                    "margin-bottom": "5px",
                                    #    "padding-bottom": "5px"
                                },
                            ),
                            dcc.Dropdown(
                                id="band",
                                placeholder="Select wavebands...",
                                clearable=True,
                                multi=True,
                                # style={"width": "50px"},
                                options=[],
                            ),
                        ]
                    )
                ),
                dbc.Row(
                    dbc.Col(
                        children=[
                            dbc.Container(
                                fluid="True",
                                # style={
                                #     # "margin-left": "0vh",
                                #     "margin-top": "0vh"},
                                children=[
                                    dmc.Text(
                                        "Date range:",  # weight=500,
                                        style={
                                            "margin-top": "20px",
                                            "margin-bottom": "5px",
                                            #    "padding-bottom": "5px"
                                        },
                                    ),
                                    dcc.DatePickerRange(
                                        id="date-picker",
                                        display_format="DD-MM-YYYY",
                                        end_date_placeholder_text="DD-MM-YYYY",
                                        start_date=None,
                                        end_date=None,
                                        style={
                                            # "width": "50px",
                                            "fontsize": "0.5rem",
                                            #    'padding-right': '50px'
                                            "margin-bottom": "300px",
                                        },
                                    ),
                                ],
                            ),
                        ],
                        #  width=8, lg=4, sm=8
                    )
                ),
            ],
        )
    ],
    # style={"height": "660px",
    #        "width": "150px",
    #        "sm": "660px"},
)

# average biases table empty data
av_bias_dict_empty = {"": "", " ": "", "  ": "", "   ": "", "    ": "", "     ": ""}
matchup_analysis_dict_empty = {
    "": (
        "Mission & Reference Site",
        "Mission Time",
        "Mission Satellite ID",
        "Cloud Percentage",
        "Satellite Viewing Angle",
        "Solar Azimuth Angle",
        "Solar Elevation",
        "AOD at 550 nm *",
        # 'Mission Product', 'Reference Product'
    ),
    " ": (
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",  # ''
    ),
}

av_bias_empty = pd.DataFrame(data=av_bias_dict_empty, index=[0])
matchup_analysis_empty = pd.DataFrame(data=matchup_analysis_dict_empty)

# create upper panel containing timeseries plot and average bias table
graph_panel_big = dmc.Card(
    # style={'height': '65vh', 'width': '120vh'},
    withBorder=True,
    shadow="xs",
    radius="md",
    children=[
        dbc.Row(
            dcc.Markdown(
                """
            **Comparison Time Series**
            """
            )
        ),
        dbc.Row(graph_upper, style={"margin-bottom": "10px"}),
        dcc.Markdown("Mean bias: "),
        dbc.Row(
            dbc.Container(
                style={
                    "margin-left": "15px",
                    #    "width": "115vh"
                },
                fluid="xs",
                children=[
                    dash_table.DataTable(
                        av_bias_empty.to_dict("records"),
                        [{"name": i, "id": i} for i in av_bias_empty.columns],
                        id="average_bias_tbl-content",
                        # fill_width=True,
                        style_cell={
                            "padding": "5px",
                            "textAlign": "left",
                            "whiteSpace": "pre-line",
                            "height": "auto",
                            "maxWidth": "20px",
                            # 'font-size': '0.8rem'
                        },
                        style_header={
                            "backgroundColor": "rgb(220, 230, 250)",
                            "fontWeight": "bold",
                            "font-size": "0.8rem",
                            "font-family": "Helvetica",
                            "whiteSpace": "normal",
                            "height": "auto",
                        },
                        style_data={
                            "color": "black",
                            "backgroundColor": "white",
                            "whiteSpace": "normal",
                            "height": "auto",
                            "font-size": "0.9rem",
                        },
                        fixed_rows={"headers": True, "data": 0},
                        style_table={"width": "115vh"},
                        css=[
                            {
                                "selector": ".dash-spreadsheet td div",
                                "rule": """
                                                      line-height: 18px; max-height: 18px; min-height: 18px; height: 18px;
                                                      display: inline-block;
                                                      word-wrap: break-word;
                                                      text-overflow: inherit;
                                                      """,
                            }
                        ],
                    )
                ],
            )
        ),
    ],
)

# combine control and upper plot panels into one row
top_panels = dmc.Container(
    fluid=True,
    children=[
        dbc.Row(
            children=[
                dbc.Col(children=[control_panel], xs=4, sm=4, md=4, lg=4),
                dbc.Col(children=[graph_panel_big], xs=8, sm=8, md=8, lg=8),
                # style={"margin-left": "10px"},
            ]
        )
    ],
)

# create bottom panel for matchup analysis table, picture of reference site location and small comparison data plot
bottom_panel = dmc.Card(
    # style={'margin-bottom': '10px', 'margin-top': '10px'},
    withBorder=True,
    shadow="xs",
    radius="md",
    children=[
        dbc.Container(
            fluid=True,
            children=[
                dbc.Row(
                    dbc.Col(
                        dcc.Markdown(
                            """
            **Matchup Analysis**
            """
                        )
                    )
                ),
                dbc.Row(
                    children=[
                        dbc.Col(
                            style={"margin-left": "2vh"},
                            children=[
                                dbc.Container(
                                    fluid="xs",
                                    children=[
                                        dash_table.DataTable(
                                            matchup_analysis_empty.to_dict("records"),
                                            [
                                                {"name": i, "id": i}
                                                for i in matchup_analysis_empty.columns
                                            ],
                                            id="matchup_analysis_tbl-content",
                                            fill_width=True,
                                            style_cell={
                                                "padding": "5px",
                                                "textAlign": "left",
                                                "whiteSpace": "pre-line",
                                                "height": "auto",
                                                "maxWidth": "20vh",
                                            },
                                            style_header={"display": "none"},
                                            style_data={
                                                "color": "black",
                                                "backgroundColor": "white",
                                                "whiteSpace": "normal",
                                                "height": "auto",
                                            },
                                            # wraps text within cells
                                            style_data_conditional=[
                                                {
                                                    "if": {"row_index": 0},
                                                    "backgroundColor": "rgb(220, 230, 250)",
                                                },
                                                # {'if': {'row_index': 'odd'},
                                                #     'backgroundColor': 'rgb(220, 230, 250)'}
                                            ],
                                            fixed_rows={"headers": False, "data": 0},
                                            css=[
                                                {
                                                    "selector": ".dash-spreadsheet td div",
                                                    "rule": """
                                                                line-height: 15px; max-height: 32px; min-height: 32px; height: 32px;
                                                                display: inline-block;
                                                                word-wrap: break-word;
                                                                text-overflow: inherit;
                                                                """,
                                                }
                                            ],  # overflow-y: visible; overflow-x: visible;
                                        ),
                                    ],
                                )
                            ],
                        ),
                        dbc.Col(
                            style={"margin-left": "4vh"},  # 'width': '450px',
                            children=[
                                dbc.Container(
                                    fluid="xs",
                                    children=[
                                        dbc.CardBody(
                                            dcc.Markdown("Scene Location")
                                        ),  # Site Map /
                                        html.Img(
                                            id="quicklook-image-content",
                                            src=f"{os.pardir}/assets/empty_quicklook.png",
                                            style={"width": "50vh"},
                                        ),
                                    ],
                                )
                            ],
                        ),
                        dbc.Col(
                            style={"margin-left": "-10vh"},
                            #'width': '500px', 'margin-right': '10px'},
                            children=[
                                dbc.Container(
                                    fluid=True,
                                    children=[
                                        dcc.Markdown("Comparison Data"),
                                        graph_dummy_small,
                                        # dcc.Markdown("Mean bias: ")
                                    ],
                                )
                            ],
                        ),
                    ]
                ),
                dbc.Row(
                    dbc.Col(
                        html.Div(
                            "* All information is from satellite product metadata, \
            except AOD which is from the RadCalNet reference site metadata.",
                            style={"padding-top": "15px"},
                        )
                    )
                ),
            ],
        )
    ],
)

layout = dmc.MantineProvider(
    html.Div(
        children=[
            dcc.Location(
                id="url",
                refresh=False,
            ),
            dcc.Interval(
                id="trigger",
                n_intervals=0,
                max_intervals=0,  # <-- only run once
                interval=1,
            ),
            dbc.Row(
                dbc.Col(
                    top_panels,
                    style={
                        "margin-top": "0vh",
                        "margin-left": "75px",
                        "margin-right": "75px",
                    },
                )
            ),
            dbc.Row(
                [
                    dbc.Col(
                        bottom_panel,
                        style={
                            "margin-top": "5vh",
                            "margin-bottom": "5vh",
                            "margin-left": "75px",
                            "margin-right": "75px",
                        },
                    )
                    # xs=12, sm=12, md=12, lg=12)
                ]
            ),
        ]
    )
)

# control panel options data for Sentinel-2, Landsat 8, Landsat 9, Planet SuperDove, Airbus Pleiades
options_s2 = [
    {"label": "B1 - 442 nm", "value": "442 nm"},
    {"label": "B2 - 492 nm", "value": "492 nm"},
    {"label": "B3 - 559 nm", "value": "559 nm"},
    {"label": "B4 - 664 nm", "value": "664 nm"},
    {"label": "B5 - 704 nm", "value": "704 nm"},
    {"label": "B6 - 740 nm", "value": "740 nm"},
    {"label": "B7 - 782 nm", "value": "782 nm"},
    {"label": "B8 - 832 nm", "value": "832 nm"},
    {"label": "B8A - 864 nm", "value": "864 nm"},
    {"label": "B9 - 945 nm", "value": "945 nm"},
    {"label": "B10 - 1373 nm", "value": "1373 nm"},
    {"label": "B11 - 1613 nm", "value": "1613 nm"},
]

options_l8 = [
    {"label": "B1 - 440 nm", "value": "440 nm"},
    {"label": "B2 - 480 nm", "value": "480 nm"},
    {"label": "B3 - 560 nm", "value": "560 nm"},
    {"label": "B4 - 660 nm", "value": "660 nm"},
    {"label": "B5 - 870 nm", "value": "870 nm"},
    {"label": "B6 - 1610 nm", "value": "1610 nm"},
    {"label": "B7 - 2200 nm", "value": "2200 nm"},
    {"label": "B9 - 1370 nm", "value": "1370 nm"},
]

options_l9 = options_l8

options_planet = [
    {"label": "B1 - 442 nm", "value": "442 nm"},
    {"label": "B2 - 490 nm", "value": "490 nm"},
    {"label": "B3 - 531 nm", "value": "531 nm"},
    {"label": "B4 - 565 nm", "value": "565 nm"},
    {"label": "B5 - 610 nm", "value": "610 nm"},
    {"label": "B6 - 665 nm", "value": "665 nm"},
    {"label": "B7 - 705 nm", "value": "705 nm"},
    {"label": "B8 - 865 nm", "value": "865 nm"},
]

options_airbus = [
    {"label": "B1 - 490 nm", "value": "490 nm"},
    {"label": "B2 - 560 nm", "value": "560 nm"},
    {"label": "B3 - 650 nm", "value": "650 nm"},
    {"label": "B4 - 840 nm", "value": "840 nm"},
]

all_options = pd.DataFrame(
    data=[options_s2, options_l8, options_l9, options_planet, options_airbus],
    index=["s2", "l8", "l9", "planetscope", "airbus_phr"],
)  # 's2a', 's2b',

all_options_dict = {
    "s2": options_s2,
    "s2a": options_s2,
    "s2b": options_s2,
    "l8": options_l8,
    "l9": options_l9,
    "planetscope": options_planet,
    "airbus_phr": options_airbus,
}


# updates control panel wavebands based on satellite selection
@callback(
    Output("band", "options", allow_duplicate=True),
    Input("sat", "value"),  # State
    # Input('trigger', 'n_intervals'),
    prevent_initial_call=True,
)
def update_band_selector(selected_sat):
    if selected_sat is None:
        return []
    return [
        {"label": band_i["label"], "value": band_i["value"]}
        for band_i in all_options_dict[selected_sat]
    ]


# updates the upper panel timeseries plot based on control panel selection
@callback(
    Output("upper-graph-content", "figure"),
    # Input('dropdown-selection', 'value')
    Input("sat", "value"),
    Input("ref", "value"),
    Input("band", "value"),
    Input("date-picker", "start_date"),
    Input("date-picker", "end_date"),
    prevent_initial_call=True,
)
def update_timeseries(sat: list, refs: list, band: list, date_1, date_2):
    empty_upper_plot = fig_empty

    if any(val is None for val in [sat, refs, band, date_1, date_2]):
        return empty_upper_plot

    else:
        date = [date_1, date_2]

        refs = sorted(refs)

        (
            timeseries_data_ref1,
            timeseries_data_ref2,
        ) = data_interface.return_timeseries_data(
            sat, refs, band, date
        )  # 2 pd dfs

        if len(timeseries_data_ref1) == 0 and len(timeseries_data_ref2) == 0:
            return empty_upper_plot

        updated_refs = []
        for ref in [timeseries_data_ref1["Ref"][0], timeseries_data_ref2["Ref"][0]]:
            if not isinstance(ref, float):
                updated_refs.append(ref)

        upper_plot = data_interface.plot_timeseries(
            sat,
            band,
            updated_refs,
            timeseries_data_ref1["Datetime"],
            timeseries_data_ref1["BiasVals"],
            timeseries_data_ref1["BiasUncVals"],
            timeseries_data_ref1["MeasValsSensor1"],
            timeseries_data_ref1["MeasValsSensor2"],
            timeseries_data_ref2["Datetime"],
            timeseries_data_ref2["BiasVals"],
            timeseries_data_ref2["BiasUncVals"],
            timeseries_data_ref2["MeasValsSensor1"],
            timeseries_data_ref2["MeasValsSensor2"],
        )

        if upper_plot == None:
            upper_plot = empty_upper_plot

    return upper_plot


# updates top panel average bias table
@callback(
    Output("average_bias_tbl-content", "data"),
    Output("average_bias_tbl-content", "columns"),
    # Input('dropdown-selection', 'value')
    Input("sat", "value"),
    Input("ref", "value"),
    Input("band", "value"),
    Input("date-picker", "start_date"),
    Input("date-picker", "end_date"),
    prevent_initial_call=True,
)
def update_bias_table(sat, refs, band, date_1, date_2):

    empty_bias_vals_table_output = (
        av_bias_empty.to_dict("records"),
        [{"name": i, "id": i} for i in av_bias_empty.columns],
    )

    if any(val is None for val in [sat, refs, band, date_1, date_2]):
        return empty_bias_vals_table_output

    else:
        date = [date_1, date_2]
        sel_refs = sorted(refs)

        (
            timeseries_data_ref1,
            timeseries_data_ref2,
        ) = data_interface.return_timeseries_data(sat, sel_refs, band, date)

        if len(timeseries_data_ref1) == 0 and len(timeseries_data_ref2) == 0:
            return empty_bias_vals_table_output

        else:
            # refs = []
            # for ref in sel_refs:
            #     if ref == timeseries_data_ref1.loc[0, "Ref"]:
            #         refs.append(ref)
            #     if ref == timeseries_data_ref2.loc[0, "Ref"]:
            #         refs.append(ref)

            updated_refs = []
            for ref in [timeseries_data_ref1["Ref"][0], timeseries_data_ref2["Ref"][0]]:
                if not isinstance(ref, float):
                    updated_refs.append(ref)

            bias_vals = data_interface.get_bias_table_vals(
                sat,
                updated_refs,
                band,
                timeseries_data_ref1["Datetime"],
                timeseries_data_ref1["BiasVals"],
                timeseries_data_ref1["BiasUncVals"],
                timeseries_data_ref1["MeasValsSensor1"],
                timeseries_data_ref1["MeasValsSensor2"],
                timeseries_data_ref2["Datetime"],
                timeseries_data_ref2["BiasVals"],
                timeseries_data_ref2["BiasUncVals"],
                timeseries_data_ref2["MeasValsSensor1"],
                timeseries_data_ref2["MeasValsSensor2"],
            )
            bias_vals_df = pd.DataFrame(data=bias_vals, index=[0])
            bias_vals_table_output = bias_vals_df.to_dict("records"), [
                {"name": i, "id": i} for i in bias_vals_df.columns
            ]

            if bias_vals == None:
                bias_vals_table_output = empty_bias_vals_table_output

    return bias_vals_table_output


# updates bottom panel parts
@callback(
    Output("small-dummy-graph-content", "figure"),
    Output("matchup_analysis_tbl-content", "data"),
    Output("matchup_analysis_tbl-content", "columns"),
    Output("quicklook-image-content", "src"),
    Input("upper-graph-content", "clickData"),
    Input("sat", "value"),
    Input("ref", "value"),
    # Input('band', 'value'),
    prevent_initial_call=True,
)
def update_bottom_panel(clickData, sat, refs):  # band

    if any(val is None for val in [clickData, sat, refs]):
        output = (
            fig_empty,
            matchup_analysis_empty.to_dict("records"),
            [{"name": i, "id": i} for i in matchup_analysis_empty.columns],
            f"{os.pardir}/assets/empty_quicklook.png",
        )
    else:
        sel_refs = sorted(refs)

        matchup_datetime = str(clickData["points"][0]["x"]).split(".")[0]

        # convert dates into comparable format
        clicked_matchup_date = datetime.datetime.strptime(
            matchup_datetime, "%Y-%m-%d %H:%M:%S"
        )
        matchup_range_end = clicked_matchup_date + datetime.timedelta(minutes=60)

        mup_info = data_interface.extract_mup_info_from_db(
            sat, sel_refs, [clicked_matchup_date, matchup_range_end]
        )

        bottom_panel_refs = []
        for ref in sel_refs:
            if ref in str(mup_info.attrs.keys()):
                bottom_panel_refs.append(ref)

        if len(bottom_panel_refs) >= 2:
            if clickData["points"][0]["curveNumber"] in [
                0,
                2,
                4,
                6,
                8,
                10,
                12,
                14,
            ]:  # only works for 2 refs for now,
                clicked_ref = [bottom_panel_refs[0]]
            else:
                clicked_ref = [bottom_panel_refs[1]]
        else:
            clicked_ref = bottom_panel_refs

        mup_info = data_interface.extract_mup_info_from_db(
            sat, clicked_ref, [clicked_matchup_date, matchup_range_end]
        )

        data, columns = data_interface.analysis_table_update(sat, clicked_ref, mup_info)

        figure = data_interface.small_plot_update(sat, clicked_ref, mup_info)

        assets_dict = {
            "RCN-GONA": "Gobabeb",
            "RCN-RVUS": "RailroadValley",
            "LIBYA-4": "libya-4-2",
        }

        if clicked_ref[0] in assets_dict.keys():
            src = f"{os.pardir}/assets/{assets_dict[clicked_ref[0]]}.png"
        else:
            src = f"{os.pardir}/assets/empty_quicklook.png"

        output = figure, data, columns, src

    return output


# runs on-load - builds the control panel and sets the options and values based on the state of the url
@callback(
    Output("sat", "value"),
    Output("band", "options"),
    Output("ref", "value"),
    Output("band", "value"),
    Output("date-picker", "start_date"),
    Output("date-picker", "end_date"),
    Input("trigger", "n_intervals"),
)
def read_url(trigger):
    out_sat = None
    out_refs = None
    out_bands = None
    out_date = [None, None]

    url = flask.request.referrer
    parts = urllib.parse.urlparse(url)
    params = urllib.parse.parse_qs(parts.query)

    if "sat" in params:
        out_sat = params["sat"][0]

    if "refs" in params:
        out_refs = []
        for i in range(len(params["refs"][0].split(","))):
            out_refs.append(params["refs"][0].split(",")[i])

    if "bands" in params:
        out_bands = []
        for i in range(len(params["bands"][0].split(","))):
            out_bands.append(params["bands"][0].split(",")[i] + " nm")

    if "date" in params:
        out_date = [params["date"][0].split(",")[0], params["date"][0].split(",")[1]]

    if out_sat is None:
        band_options = []
    else:
        band_options = [
            {"label": band_i["label"], "value": band_i["value"]}
            for band_i in all_options_dict[out_sat]
        ]

    return out_sat, band_options, out_refs, out_bands, out_date[0], out_date[1]


# updates url based on control panel selection
@callback(
    Output("url", "search"),
    Input("sat", "value"),
    Input("ref", "value"),
    Input("band", "value"),
    Input("date-picker", "start_date"),
    Input("date-picker", "end_date"),
    prevent_initial_call=True,
)
def display_page(sat, ref, band, date_1, date_2):
    vals = [sat, ref, band, [date_1, date_2]]
    vars = ["sat", "refs", "bands", "date"]

    search_output = "?"
    for i, val in enumerate(vals):
        if val is not None:
            if i == 0:  # sat
                search_output += f"{vars[i]}={val}&"
            elif i == 1:  # refs
                url_refs = ""
                for k in val:
                    url_refs += f"{k},"
                url_refs = url_refs[:-1]
                search_output += f"{vars[i]}={url_refs}&"
            elif i == 2:
                url_bands = ""
                for k in val:
                    url_bands += f"{k[:-3]},"
                url_bands = url_bands[:-1]
                search_output += f"{vars[i]}={url_bands}&"
            elif i == 3:
                url_dates = ""
                if val != [None, None]:
                    for k in val:
                        if k is not None:
                            url_dates += f"{k},"
                    url_dates = url_dates[:-1]
                    search_output += f"{vars[i]}={url_dates}&"

    search_output = search_output[:-1]

    return search_output
