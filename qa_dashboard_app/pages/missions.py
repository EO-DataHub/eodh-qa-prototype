import dash
from dash import html, dcc, callback, Input, Output
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc

dash.register_page(
    __name__,
    order=6,
    title="Calibration Dashboard - Missions information",  # name of tab
    # image='missions.png',  # metadata
    description="Further information on the missions.",  # metadata
    location="sidebar",
)

HEIGHT_OF_ROW = 345

layout = dmc.MantineProvider(
    html.Div(
        [
            html.H1(
                "Content coming soon.",
                style={
                    "margin-top": "5vh",
                    "margin-left": "75px",
                    "margin-right": "75px",
                },
            ),
            html.Div(
                "This page will display information on all the missions contributing to CEOS-PVP.",
                style={
                    "margin-top": "5vh",
                    "margin-bottom": "75px",
                    "margin-left": "75px",
                    "margin-right": "75px",
                },
            ),
        ]
    )
)
