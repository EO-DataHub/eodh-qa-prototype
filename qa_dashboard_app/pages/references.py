import dash
from dash import html, dcc, dash_table, callback, Input, Output
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
import pandas as pd

dash.register_page(
    __name__,
    order=4,
    title="RadVAL - References",  # name of tab
    # image='references.png',  # metadata
    description="Reference information.",  # metadata
    location="sidebar",
)

HEIGHT_OF_ROW = 345

l4_site_info_dict = {
    "Reference Site": (
        "Location",
        "Instrumented or Pseudo-Invariant Calibration Site (PICS)",
        "Surface type",
        "Coordinates",
    ),
    "Libya 4": ("Libya", "PICS", "Desert sand", "28.55 N, 23.39 E"),
}
l4_site_info_df = pd.DataFrame(data=l4_site_info_dict)

# libya 4 box
libya4_box = dmc.Card(
    children=[
        dbc.Row(
            children=[
                dbc.Col(
                    dmc.Container(
                        fluid=True,
                        children=[
                            html.Img(
                                id="libya-4_image",
                                src="assets/Libya-4-CenterROI-GoogleEarth.png",
                                style={"width": "50vh", "margin-bottom": "5vh"},
                            )
                        ],
                    )
                ),
                dbc.Col(
                    dbc.Container(
                        style={
                            "margin-top": "25px",
                            "width": "80vh",
                            # 'margin-left': '15px', 'margin-right': '20px',
                        },
                        fluid="xs",
                        children=[
                            dash_table.DataTable(
                                l4_site_info_df.to_dict("records"),
                                [{"name": i, "id": i} for i in l4_site_info_df.columns],
                                id="libya-4_tbl-content",
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
                                    "font-size": "1.4rem",
                                    "font-family": "Helvetica",
                                    "whiteSpace": "normal",
                                    "height": "auto",
                                },
                                style_data={
                                    "color": "black",
                                    "backgroundColor": "white",
                                    "whiteSpace": "normal",
                                    "height": "auto",
                                    "font-size": "1.1rem",
                                },
                                fixed_rows={"headers": True, "data": 0},
                            )
                        ],
                    )
                ),
            ]
        )
    ]
)

gona_site_info_dict = {
    "Reference Site": (
        "Location",
        "Instrumented or Pseudo-Invariant Calibration Site (PICS)",
        "Surface type",
        "Coordinates",
    ),
    "RCN - GONA": (
        "Gobabeb, Namibia",
        "Instrumented (RadCalNet) operated by European Space Agency (ESA) and CNES",
        "Desert sand",
        "23.6 S, 15.1196 E",
    ),
}
gona_site_info_df = pd.DataFrame(data=gona_site_info_dict)

# gona box
gona_box = dmc.Card(  # withBorder=True, shadow="xs", radius="md",
    children=[
        dbc.Row(
            children=[
                dbc.Col(
                    dmc.Container(
                        fluid=True,
                        children=[
                            html.Img(
                                id="gona_image",
                                src="assets/Gobabeb.png",
                                style={"width": "50vh", "margin-bottom": "5vh"},
                            )
                        ],
                    )
                ),
                dbc.Col(
                    dbc.Container(
                        style={
                            "margin-top": "25px",
                            "width": "80vh",
                            # 'margin-left': '15px', 'margin-right': '20px',
                        },
                        fluid="xs",
                        children=[
                            dash_table.DataTable(
                                gona_site_info_df.to_dict("records"),
                                [
                                    {"name": i, "id": i}
                                    for i in gona_site_info_df.columns
                                ],
                                id="gona_tbl-content",
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
                                    "font-size": "1.4rem",
                                    "font-family": "Helvetica",
                                    "whiteSpace": "normal",
                                    "height": "auto",
                                },
                                style_data={
                                    "color": "black",
                                    "backgroundColor": "white",
                                    "whiteSpace": "normal",
                                    "height": "auto",
                                    "font-size": "1.1rem",
                                },
                                fixed_rows={"headers": True, "data": 0},
                            )
                        ],
                    )
                ),
            ]
        )
    ]
)

rvus_site_info_dict = {
    "Reference Site": (
        "Location",
        "Instrumented or Pseudo-Invariant Calibration Site (PICS)",
        "Surface type",
        "Coordinates",
    ),
    "RCN - RVUS": (
        "Railroad Valley Playa, USA",
        "Instrumented (RadCalNet) operated by the University of Arizona",
        "Clay-based playa",
        "38.497 N and 115.690 W",
    ),
}
rvus_site_info_df = pd.DataFrame(data=rvus_site_info_dict)

# rvus box
rvus_box = dmc.Card(  # withBorder=True, shadow="xs", radius="md",
    children=[
        dbc.Row(
            children=[
                dbc.Col(
                    dmc.Container(
                        fluid=True,
                        children=[
                            html.Img(
                                id="rvus_image",
                                src="assets/RailroadValley.png",
                                style={"width": "50vh", "margin-bottom": "5vh"},
                            )
                        ],
                    )
                ),
                dbc.Col(
                    dbc.Container(
                        style={
                            "margin-top": "25px",
                            "width": "80vh",
                            # 'margin-left': '15px', 'margin-right': '20px',
                        },
                        fluid="xs",
                        children=[
                            dash_table.DataTable(
                                rvus_site_info_df.to_dict("records"),
                                [
                                    {"name": i, "id": i}
                                    for i in rvus_site_info_df.columns
                                ],
                                id="rvus_tbl-content",
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
                                    "font-size": "1.4rem",
                                    "font-family": "Helvetica",
                                    "whiteSpace": "normal",
                                    "height": "auto",
                                },
                                style_data={
                                    "color": "black",
                                    "backgroundColor": "white",
                                    "whiteSpace": "normal",
                                    "height": "auto",
                                    "font-size": "1.1rem",
                                },
                                fixed_rows={"headers": True, "data": 0},
                            )
                        ],
                    )
                ),
            ]
        )
    ]
)

lake_tahoe_site_info_dict = {
    "Reference Site": (
        "Location",
        "Instrumented or Pseudo-Invariant Calibration Site (PICS)",
        "Surface type",
        "Coordinates",
    ),
    "RCN - Lake Tahoe": (
        "California, USA",
        "Instrumented (RadCalNet) operated by NASA Jet Propulsion Lab (JPL)",
        "Water",
        "39.12488 N, 120.03927 W",
    ),
}
lake_tahoe_site_info_df = pd.DataFrame(data=lake_tahoe_site_info_dict)

# lake tahoe box
lake_tahoe_box = dmc.Card(  # withBorder=True, shadow="xs", radius="md",
    children=[
        dbc.Row(
            children=[
                dbc.Col(
                    dmc.Container(
                        fluid=True,
                        children=[
                            html.Img(
                                id="lake_tahoe_image",
                                src="assets/LakeTahoezoom.jpg",
                                style={"width": "50vh", "margin-bottom": "5vh"},
                            )
                        ],
                    )
                ),
                dbc.Col(
                    dbc.Container(
                        style={
                            "margin-top": "25px",
                            "width": "80vh",
                            # 'margin-left': '15px', 'margin-right': '20px',
                        },
                        fluid="xs",
                        children=[
                            dash_table.DataTable(
                                lake_tahoe_site_info_df.to_dict("records"),
                                [
                                    {"name": i, "id": i}
                                    for i in lake_tahoe_site_info_df.columns
                                ],
                                id="lake-tahoe_tbl-content",
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
                                    "font-size": "1.4rem",
                                    "font-family": "Helvetica",
                                    "whiteSpace": "normal",
                                    "height": "auto",
                                },
                                style_data={
                                    "color": "black",
                                    "backgroundColor": "white",
                                    "whiteSpace": "normal",
                                    "height": "auto",
                                    "font-size": "1.1rem",
                                },
                                fixed_rows={"headers": True, "data": 0},
                            )
                        ],
                    )
                ),
            ]
        )
    ]
)

l1_site_info_dict = {
    "Reference Site": (
        "Location",
        "Instrumented or Pseudo-Invariant Calibration Site (PICS)",
        "Surface type",
        "Coordinates",
    ),
    "Libya 1": ("Libya", "PICS", "Desert sand", "24.42 N, 13.35 E"),
}
l1_site_info_df = pd.DataFrame(data=l1_site_info_dict)

# libya 4 box
libya1_box = dmc.Card(
    children=[
        dbc.Row(
            children=[
                dbc.Col(
                    dmc.Container(
                        fluid=True,
                        children=[
                            html.Img(
                                id="libya-1_image",
                                src="assets/Libya-1-CenterROI-GoogleEarth.png",
                                style={"width": "50vh", "margin-bottom": "5vh"},
                            )
                        ],
                    )
                ),
                dbc.Col(
                    dbc.Container(
                        style={
                            "margin-top": "25px",
                            "width": "80vh",
                            # 'margin-left': '15px', 'margin-right': '20px',
                        },
                        fluid="xs",
                        children=[
                            dash_table.DataTable(
                                l1_site_info_df.to_dict("records"),
                                [{"name": i, "id": i} for i in l1_site_info_df.columns],
                                id="libya-1_tbl-content",
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
                                    "font-size": "1.4rem",
                                    "font-family": "Helvetica",
                                    "whiteSpace": "normal",
                                    "height": "auto",
                                },
                                style_data={
                                    "color": "black",
                                    "backgroundColor": "white",
                                    "whiteSpace": "normal",
                                    "height": "auto",
                                    "font-size": "1.1rem",
                                },
                                fixed_rows={"headers": True, "data": 0},
                            )
                        ],
                    )
                ),
            ]
        )
    ]
)


alg3_site_info_dict = {
    "Reference Site": (
        "Location",
        "Instrumented or Pseudo-Invariant Calibration Site (PICS)",
        "Surface type",
        "Coordinates",
    ),
    "Algeria 3": ("Algeria", "PICS", "Desert sand", "30.32 N, 7.66 E"),
}
alg3_site_info_df = pd.DataFrame(data=alg3_site_info_dict)

# algeria 3 box
algeria3_box = dmc.Card(
    children=[
        dbc.Row(
            children=[
                dbc.Col(
                    dmc.Container(
                        fluid=True,
                        children=[
                            html.Img(
                                id="algeria-3_image",
                                src="assets/Algeria-3-centerROI-GoogleEarth.png",
                                style={"width": "50vh", "margin-bottom": "5vh"},
                            )
                        ],
                    )
                ),
                dbc.Col(
                    dbc.Container(
                        style={
                            "margin-top": "25px",
                            "width": "80vh",
                            # 'margin-left': '15px', 'margin-right': '20px',
                        },
                        fluid="xs",
                        children=[
                            dash_table.DataTable(
                                alg3_site_info_df.to_dict("records"),
                                [
                                    {"name": i, "id": i}
                                    for i in alg3_site_info_df.columns
                                ],
                                id="algeria-3_tbl-content",
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
                                    "font-size": "1.4rem",
                                    "font-family": "Helvetica",
                                    "whiteSpace": "normal",
                                    "height": "auto",
                                },
                                style_data={
                                    "color": "black",
                                    "backgroundColor": "white",
                                    "whiteSpace": "normal",
                                    "height": "auto",
                                    "font-size": "1.1rem",
                                },
                                fixed_rows={"headers": True, "data": 0},
                            )
                        ],
                    )
                ),
            ]
        )
    ]
)

baotou_geo_info_dict = {
    "Reference Site": (
        "Location",
        "Operated by",
        "Surface type",
        "Coordinates",
    ),
    "Baotou Target": (
        "Baotou City, Inner Mongolia, China",
        "Academy of Opto-Electronics, Chinese Academy of Sciences",
        "Gravel",
        "N 40.854, E 109.628",
    ),
}
baotou_geo_info_df = pd.DataFrame(data=baotou_geo_info_dict)

# baotou_geo box
baotou_geo_box = dmc.Card(  # withBorder=True, shadow="xs", radius="md",
    children=[
        dbc.Row(
            children=[
                dbc.Col(
                    dmc.Container(
                        fluid=True,
                        children=[
                            html.Img(
                                id="baotou_geo_image",
                                src="assets/Baotou_geo.png",
                                style={"width": "50vh", "margin-bottom": "5vh"},
                            )
                        ],
                    )
                ),
                dbc.Col(
                    dbc.Container(
                        style={
                            "margin-top": "25px",
                            "width": "80vh",
                            # 'margin-left': '15px', 'margin-right': '20px',
                        },
                        fluid="xs",
                        children=[
                            dash_table.DataTable(
                                baotou_geo_info_df.to_dict("records"),
                                [
                                    {"name": i, "id": i}
                                    for i in baotou_geo_info_df.columns
                                ],
                                id="baotou-geo_tbl-content",
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
                                    "font-size": "1.4rem",
                                    "font-family": "Helvetica",
                                    "whiteSpace": "normal",
                                    "height": "auto",
                                },
                                style_data={
                                    "color": "black",
                                    "backgroundColor": "white",
                                    "whiteSpace": "normal",
                                    "height": "auto",
                                    "font-size": "1.1rem",
                                },
                                fixed_rows={"headers": True, "data": 0},
                            )
                        ],
                    )
                ),
            ]
        )
    ]
)


shadnagar_info_dict = {
    "Reference Site": (
        "Location",
        "Operated by",
        "Surface type",
        "Coordinates",
    ),
    "Shadnagar Target": (
        "Hyderabad, Telangana, India",
        "ISRO National Remote Sensing Centre (NRSC)",
        "Mixture of soil, stone and gravel",
        "17.033 N, 78.183 E",
    ),
}
shadnagar_info_df = pd.DataFrame(data=shadnagar_info_dict)

# shadnagar box
shadnagar_box = dmc.Card(  # withBorder=True, shadow="xs", radius="md",
    children=[
        dbc.Row(
            children=[
                dbc.Col(
                    dmc.Container(
                        fluid=True,
                        children=[
                            html.Img(
                                id="shadnagar_image",
                                src="assets/Shadnagar_geo.png",
                                style={"width": "50vh", "margin-bottom": "5vh"},
                            )
                        ],
                    )
                ),
                dbc.Col(
                    dbc.Container(
                        style={
                            "margin-top": "25px",
                            "width": "80vh",
                            # 'margin-left': '15px', 'margin-right': '20px',
                        },
                        fluid="xs",
                        children=[
                            dash_table.DataTable(
                                shadnagar_info_df.to_dict("records"),
                                [
                                    {"name": i, "id": i}
                                    for i in shadnagar_info_df.columns
                                ],
                                id="shadnagar_tbl-content",
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
                                    "font-size": "1.4rem",
                                    "font-family": "Helvetica",
                                    "whiteSpace": "normal",
                                    "height": "auto",
                                },
                                style_data={
                                    "color": "black",
                                    "backgroundColor": "white",
                                    "whiteSpace": "normal",
                                    "height": "auto",
                                    "font-size": "1.1rem",
                                },
                                fixed_rows={"headers": True, "data": 0},
                            )
                        ],
                    )
                ),
            ]
        )
    ]
)

kf_causeway_info_dict = {
    "Reference Site": (
        "Location",
        "Operated by",
        "Surface type",
        "Coordinates",
    ),
    "King Fahd Causeway": (
        "Gulf of Bahrain, Saudi Arabia/Bahrain",
        "N/A",
        "N/A",
        "26.182 N, 50.338 E",
    ),
}
kf_causeway_info_df = pd.DataFrame(data=kf_causeway_info_dict)

# kf_causeway box
kf_causeway_box = dmc.Card(  # withBorder=True, shadow="xs", radius="md",
    children=[
        dbc.Row(
            children=[
                dbc.Col(
                    dmc.Container(
                        fluid=True,
                        children=[
                            html.Img(
                                id="kf_causeway_image",
                                src="assets/King_fahd_SA-B.png",
                                style={"width": "60vh", "margin-bottom": "5vh"},
                            )
                        ],
                    )
                ),
                dbc.Col(
                    dbc.Container(
                        style={  #'margin-top': '25px',
                            "width": "80vh",
                            # 'margin-left': '15px', 'margin-right': '20px',
                        },
                        fluid="xs",
                        children=[
                            dash_table.DataTable(
                                kf_causeway_info_df.to_dict("records"),
                                [
                                    {"name": i, "id": i}
                                    for i in kf_causeway_info_df.columns
                                ],
                                id="kf-causeway_tbl-content",
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
                                    "font-size": "1.4rem",
                                    "font-family": "Helvetica",
                                    "whiteSpace": "normal",
                                    "height": "auto",
                                },
                                style_data={
                                    "color": "black",
                                    "backgroundColor": "white",
                                    "whiteSpace": "normal",
                                    "height": "auto",
                                    "font-size": "1.1rem",
                                },
                                fixed_rows={"headers": True, "data": 0},
                            )
                        ],
                    )
                ),
            ]
        )
    ]
)


lake_pontchartrain_info_dict = {
    "Reference Site": (
        "Location",
        "Operated by",
        "Surface type",
        "Coordinates",
    ),
    "Lake Pontchartrain Causeway": (
        "New Orleans, Lousiana, USA",
        "N/A",
        "N/A",
        "30.212 N, 90.121 W",
    ),
}
lake_pontchartrain_info_df = pd.DataFrame(data=lake_pontchartrain_info_dict)

# lake_pontchartrain box
lake_pontchartrain_box = dmc.Card(  # withBorder=True, shadow="xs", radius="md",
    children=[
        dbc.Row(
            children=[
                dbc.Col(
                    dmc.Container(
                        fluid=True,
                        children=[
                            html.Img(
                                id="lake_pontchartrain_image",
                                src="assets/LakePontchartrain.png",
                                style={"width": "60vh", "margin-bottom": "5vh"},
                            )
                        ],
                    )
                ),
                dbc.Col(
                    dbc.Container(
                        style={  #'margin-top': '25px',
                            "width": "80vh",
                            # 'margin-left': '15px', 'margin-right': '20px',
                        },
                        fluid="xs",
                        children=[
                            dash_table.DataTable(
                                lake_pontchartrain_info_df.to_dict("records"),
                                [
                                    {"name": i, "id": i}
                                    for i in lake_pontchartrain_info_df.columns
                                ],
                                id="lake-pont_tbl-content",
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
                                    "font-size": "1.4rem",
                                    "font-family": "Helvetica",
                                    "whiteSpace": "normal",
                                    "height": "auto",
                                },
                                style_data={
                                    "color": "black",
                                    "backgroundColor": "white",
                                    "whiteSpace": "normal",
                                    "height": "auto",
                                    "font-size": "1.1rem",
                                },
                                fixed_rows={"headers": True, "data": 0},
                            )
                        ],
                    )
                ),
            ]
        )
    ]
)

rad_sites_card = dmc.Card(
    withBorder=True,
    shadow="xs",
    radius="md",
    children=[
        html.H2(
            "Radiometric sites:",
            # style={'margin-top': '5vh',
            #      'margin-left': '75px',
            #      'margin-right': '75px'}
        ),
        # dbc.Row(children=[
        #     dbc.Col(gona_box),
        #     dbc.Col(rvus_box)]),
        dbc.Row(children=[gona_box]),
        dbc.Row(children=[rvus_box]),
        dbc.Row(children=[lake_tahoe_box]),
        dbc.Row(children=[libya4_box]),
        dbc.Row(children=[libya1_box]),
        dbc.Row(children=[algeria3_box]),
    ],
    # style={'margin-left': '10px'},
)

geo_sites_card = dmc.Card(
    withBorder=True,
    shadow="xs",
    radius="md",
    children=[
        html.H2(
            "Geometric sites:",
            # style={'margin-top': '5vh',
            #      'margin-left': '75px',
            #      'margin-right': '75px'}
        ),
        dbc.Row(children=[baotou_geo_box]),
        dbc.Row(children=[shadnagar_box]),
        dbc.Row(children=[kf_causeway_box]),
        dbc.Row(children=[lake_pontchartrain_box]),
    ],
    # style={'margin-left': '10px'},
)


layout = dmc.MantineProvider(
    html.Div(
        [
            dbc.Row(
                rad_sites_card,
                style={
                    "margin-top": "5vh",
                    "margin-bottom": "5vh",
                    "margin-left": "75px",
                    "margin-right": "75px",
                },
            ),
            dbc.Row(
                geo_sites_card,
                style={
                    "margin-top": "5vh",
                    "margin-bottom": "5vh",
                    "margin-left": "75px",
                    "margin-right": "75px",
                },
            ),
        ]
    )
)
