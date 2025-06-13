import dash
from dash import html, dcc, callback, Input, Output

dash.register_page(
    __name__,
    order=6,
    title="Calibration Dashboard - Missions information",  # name of tab
    # image='missions.png',
    description="Further information on the missions.",
    location="sidebar",
)

HEIGHT_OF_ROW = 345

layout = html.Div(
    [
        html.H1(
            "This is our Missions page",
            style={"margin-top": "5vh", "margin-left": "75px", "margin-right": "75px"},
        ),
        html.Div(
            "This is our Missions page content.",
            style={
                "margin-top": "5vh",
                "margin-bottom": "75px",
                "margin-left": "75px",
                "margin-right": "75px",
            },
        ),
    ]
)
