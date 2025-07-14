import dash
from dash import html
import dash_mantine_components as dmc

dash.register_page(
    __name__,
    order=7,
    title="Click a button to return to the app",  # name of tab
    description="404",  # metadata
    location="None",
)

HEIGHT_OF_ROW = 345

layout = dmc.MantineProvider(
    html.H2(
        "Please click CEOS-PVP Homepage to return to the homepage.",
        style={
            "margin-top": "5vh",
            "margin-bottom": "75px",
            "margin-left": "75px",
            "margin-right": "75px",
        },
    )
)
