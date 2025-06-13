import dash
from dash import html, dcc, callback, Input, Output
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc

dash.register_page(
    __name__,
    order=3,
    title="Calibration Dashboard - Help",  # name of tab
    # image='help.png',
    description="Further help and FAQs.",
    location="sidebar",
)

HEIGHT_OF_ROW = 345

# description box
descr_box = dmc.Card(
    withBorder=True,
    shadow="xs",
    radius="md",
    children=[
        html.H2(
            "What is the CEOS Calibration Dashboard?",
            # style={'margin-top': '5vh',
            #      'margin-left': '75px',
            #      'margin-right': '75px'}
        ),
        # html.P(
        html.Div(
            dcc.Markdown(
                """This dashboard displays the results from radiometric comparisons between a mission data \
                                      collection (e.g. Sentinel-2 L1C, Planet SuperDove L3B) and RadCalNet in-situ sites. See [CEOS WGCV RadCalNet](https://ceos.org/home-2/wgcv-radcalnet/) for more information \
                                      on the RadCalNet sites.""",
                link_target="_blank",
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
how_to_box = dmc.Card(
    withBorder=True,
    shadow="xs",
    radius="md",
    children=[
        html.H2(
            "How to navigate the dashboard:",
            # style={'margin-top': '5vh',
            #        'margin-left': '75px',
            #        'margin-right': '75px'}
        ),
        html.Div(
            dcc.Markdown(
                """
                                            1. Make a selection of mission, reference site(s), bands and date range of interest. 
                                            2. View an interactive plot for the timeseries of data from matchups according to your selection.
                                            3. Select a specific point of interest from the plot, referring to one matchup between the selected satellite mission and reference site.
                                            4. Scroll down to see more detailed information for that matchup.
                      """
            ),
            # style={'margin-top': '5vh',
            #        'margin-bottom': '75px',
            #        'margin-left': '75px',
            #        'margin-right': '75px'}
        ),
    ],
)

# EODH descr box
eodh_card = dmc.Card(
    withBorder=True,
    shadow="xs",
    radius="md",
    children=[
        dbc.CardImg(
            src="assets/powered_by_eodh.png",
            top=True,
            style={"width": "25rem", "margin-bottom": "20px"},
        ),
        dbc.CardBody(
            html.Div(
                dcc.Markdown(
                    """ The EODH can be accessed at: [staging.eodatahub.org.uk]("https://staging.eodatahub.org.uk/").  
                            The EODH is a centralised software infrastructure, \
                            providing a new ‘single point’ of access for EO data offerings from both public and commercial sources \
                            where you can carry out analyses, as well as access QA information for a range of missions.  
                            The EODH STAC catalog entry for the data collection selected on the CEOS Dashboard can be accessed at the link provided. 
                                                    """,
                    link_target="_blank",
                    style={"text-align": "justify"},
                ),
                className="card-text",
            )
        ),
    ],
    # style={"width": "25rem"},
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
                                dbc.Col(descr_box),  # xs=2, sm=2, md=2, lg=2,
                                dbc.Col(
                                    how_to_box,  # xs=2, sm=2, md=2, lg=2,
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
                                dbc.Col(eodh_card),
                                dbc.Col(descr_box),  # xs=2, sm=2, md=2, lg=2,
                                dbc.Col(
                                    how_to_box,  # xs=2, sm=2, md=2, lg=2,
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
