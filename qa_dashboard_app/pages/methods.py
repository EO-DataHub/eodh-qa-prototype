import dash
from dash import html, dcc, callback, Input, Output

dash.register_page(
    __name__,
    order=4,
    title="Calibration Dashboard - Methods",  # name of tab
    # image='methods.png',
    description="Further information on methods.",
    location="sidebar",
)

HEIGHT_OF_ROW = 345

layout = html.Div(
    [
        html.H1(
            "This is our Methods page",
            style={"margin-top": "5vh", "margin-left": "75px", "margin-right": "75px"},
        ),
        html.Div(
            "ATBD to be added.",
            style={
                "margin-top": "5vh",
                "margin-bottom": "75px",
                "margin-left": "75px",
                "margin-right": "75px",
            },
        ),
    ]
)
