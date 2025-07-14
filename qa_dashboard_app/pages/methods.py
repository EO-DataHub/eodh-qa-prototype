import dash
from dash import html, dcc, callback, Input, Output
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc

dash.register_page(
    __name__,
    order=4,
    title="Calibration Dashboard - Methods",  # name of tab
    # image='methods.png',  # metadata
    description="Further information on methods.",  # metadata
    location="sidebar",
)

HEIGHT_OF_ROW = 345

# description box
atbd_box = dmc.Card(
    withBorder=True,
    shadow="xs",
    radius="md",
    children=[
        html.H2(
            "ATBD to be added",
        ),
        html.Div(
            dcc.Markdown(
                """ATBD to be added.""",
                link_target="_blank",
                style={"text-align": "justify"},
            ),
        ),
    ],
)

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
                "This page will display the methods and algorithms used to create the comparisons displayed on the RadVAL dashboard.",
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
