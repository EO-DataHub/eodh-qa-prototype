import dash
from dash import html, dcc, callback, Input, Output
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc

dash.register_page(
    __name__,
    order=1,
    name="CEOS Activity",
    # path = '/',
    title="CEOS Activity",  # name of tab
    # image='ceos_activity.png',
    description="Description of CEOS activity.",
    location="sidebar",
)


HEIGHT_OF_ROW = 345

# outline box
outline_box = dmc.Card(
    withBorder=True,
    shadow="xs",
    radius="md",
    children=[
        html.H2(
            "What is this activity and why is it important?",
            # style={'margin-top': '5vh',
            #      'margin-left': '75px',
            #      'margin-right': '75px'}
        ),
        # html.P(
        html.Div(
            dcc.Markdown(
                """Description of the activity.                                                         
                                   """,
                style={"text-align": "justify"},
            ),
            # style={'margin-top': '5vh',
            #        'margin-bottom': '75px',
            #        'margin-left': '75px',
            #        'margin-right': '75px'}
        ),
    ],
)

# how-to box
howto_box = dmc.Card(
    withBorder=True,
    shadow="xs",
    radius="md",
    children=[
        html.H2(
            "How do I contribute my Mission data?",
            # style={'margin-top': '5vh',
            #      'margin-left': '75px',
            #      'margin-right': '75px'}
        ),
        # html.P(
        html.Div(
            dcc.Markdown(
                """Description of how to contribute.""", style={"text-align": "justify"}
            ),
            # style={'margin-top': '5vh',
            #        'margin-bottom': '75px',
            #        'margin-left': '75px',
            #        'margin-right': '75px'}
        ),
    ],
)

layout = html.Div(
    [
        dbc.Row(
            dbc.Col(
                dmc.Container(
                    fluid=True,
                    children=[
                        dbc.Row(
                            children=[
                                dbc.Col(outline_box),  # xs=2, sm=2, md=2, lg=2,
                                dbc.Col(
                                    outline_box,  # xs=2, sm=2, md=2, lg=2,
                                    # style={'margin-left': '10px'},
                                ),
                            ]
                        )
                    ],
                )
            ),
            style={"margin-top": "0vh", "margin-left": "75px", "margin-right": "75px"},
        ),
        dbc.Row(
            dbc.Col(
                dmc.Container(
                    fluid=True,
                    children=[
                        dbc.Row(
                            children=[
                                dbc.Col(howto_box),
                                dbc.Col(howto_box),  # xs=2, sm=2, md=2, lg=2,
                                dbc.Col(
                                    howto_box,  # xs=2, sm=2, md=2, lg=2,
                                ),
                            ]
                        )
                    ],
                )
            ),
            style={
                "margin-top": "5vh",
                "margin-bottom": "5vh",
                "margin-left": "75px",
                "margin-right": "75px",
            },
        ),
    ]
)
