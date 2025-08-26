import dash
from dash import html, dcc, callback, Input, Output
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc

dash.register_page(
    __name__,
    order=3,
    name="CID and Sensors",
    title="RadVAL - CID & Sensors",  # name of tab
    # image='missions.png',  # metadata
    description="Further information on the data collected within the CID and contributing sensor characteristics.",  # metadata
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
                "This page will display the data collected within the Comparison Image Database (CID) "
                "that populate the RadVal tool, alongside a description of the basic characteristics for"
                " the sensors contributing to the CEOS-PVP activity. This is comprised of information that "
                "the data providers have agreed to make public and, if applicable, will link to the sensor "
                "operator for further information.",
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
