import dash
from dash import html, dcc, callback, Input, Output
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc

dash.register_page(
    __name__,
    order=1,
    name="CEOS-PVP Homepage",
    path="/",
    title="CEOS-PVP",  # name of tab
    description="Description of CEOS-Product Validation Platform activity.",  # metadata
    location="sidebar",
)


HEIGHT_OF_ROW = 345

# rad_sites img
rad_sites = dmc.Card(
    withBorder=True,
    shadow="xs",
    radius="md",
    children=[
        html.Img(
            id="rad_sites_image", src="assets/rad_sites.png", style={"width": "80vh"}
        ),
        html.Div(
            dcc.Markdown(
                """For detailed information on each of the sites, 
                               including their coordinates, please visit the [*_References_*](./references) tab at the top of the page.
                                """,
                style={"text-align": "justify", "margin-top": "5vh"},
            )
        ),
    ],
)

# geo_sites img
geo_sites = dmc.Card(
    withBorder=True,
    shadow="xs",
    radius="md",
    children=[
        html.Img(
            id="geo_sites_image", src="assets/geo_sites.png", style={"width": "80vh"}
        ),
        html.Div(
            dcc.Markdown(
                """For detailed information on each of the sites, 
                               including their coordinates, please visit the [*_References_*](./references) tab at the top of the page.
                                """,
                style={"text-align": "justify", "margin-top": "5vh"},
            )
        ),
    ],
)

# rad_geo_sites box
rad_geo_sites_box = dmc.Card(
    withBorder=True,
    shadow="xs",
    radius="md",
    children=[
        html.Img(
            id="rad_sites_image",
            src="assets/rad_sites.png",
            style={"width": "80vh", "margin-bottom": "5vh"},
        ),
        html.Img(
            id="geo_sites_image", src="assets/geo_sites.png", style={"width": "80vh"}
        ),
        html.Div(
            dcc.Markdown(
                """For detailed information on each of the sites, 
                               including their coordinates, please visit the [*_References_*](./references) tab at the top of the page.
                                """,
                style={"text-align": "justify", "margin-top": "5vh"},
            )
        ),
    ],
)

# ceos-pvp_breakdown img
ceos_pvp_breakdown = dmc.Card(
    withBorder=True,
    shadow="xs",
    radius="md",
    children=[
        html.H2("CEOS-PVP Architecture:", style={"margin-bottom": "5vh"}),
        html.Img(
            id="ceos-pvp_breakdown_image",
            src="assets/ceos-pvp_breakdown.png",
            style={
                "width": "80vh",
                "margin-left": "25px",
            },
        ),
    ],
)


# outline box
outline_box = dmc.Card(
    withBorder=True,
    shadow="xs",
    radius="md",
    children=[
        html.H2(
            "What is the CEOS-PVP Activity?",
            # style={'margin-top': '5vh',
            #      'margin-left': '75px',
            #      'margin-right': '75px'}
        ),
        # html.P(
        html.Div(
            dcc.Markdown(
                """An initiative led by CEOS WGCV, following requests 
                                   of the ‘new space’/commercial satellite community, the Product Validation Platform 
                                   (CEOS-PVP) aims to benefit the whole EO community. This platform will allow satellite 
                                   data providers, CEOS agencies and others, to evidence the quality of their data in a
                                    consistent manner through comparison to a community agreed reference using a minimal 
                                    set of established calibration sites (including RadCalNet and PICS). This data will
                                     be compiled into the Comparison Image Database (CID) as an open accessible record 
                                     of capability. Initially this will be limited to optical geometric and radiometric sensors.                                          
                                   """,
                style={"text-align": "justify"},
            ),
            # style={'margin-top': '5vh',
            #        'margin-bottom': '75px',
            #        'margin-left': '75px',
            #        'margin-right': '75px'}
        ),
        html.Div(
            dcc.Markdown(
                """The radiometric data from the CID is additionally used 
                                to populate the RadVAL (Radiometric Validation & AnaLytics) interactive dashboard tool, 
                                available under the [*_RadVAL Dashboard_*](./radval-dashboard) tab at the top of this page, which aims to visually 
                                evidence 'performance' against an internationally accepted reference, independent of any
                                 specific sensor but with the means to identify biases against any sensor in the database.                                                 
                                                                   """,
                style={"text-align": "justify"},
            ),
            # style={'margin-top': '5vh',
            #        'margin-bottom': '75px',
            #        'margin-left': '75px',
            #        'margin-right': '75px'}
        ),
        html.Div(
            dcc.Markdown(
                """Future plans include extending this system to support 
                               validation of other data metrics, e.g. surface reflectance, SAR and other sensor products. 
                                            """,
                style={"text-align": "justify"},
            ),  # while also receiving feedback from ??? on ???
            # style={'margin-top': '5vh',
            #        'margin-bottom': '75px',
            #        'margin-left': '75px',
            #        'margin-right': '75px'}
        ),
        html.Div(
            dcc.Markdown(
                """Through contributing, data providers will be able to
                                 demonstrate their radiometric performance and stability to all users in a consistent
                                  manner via a range of independent references.
                                            """,
                style={"text-align": "justify"},
            ),  # while also receiving feedback from ??? on ???
            # style={'margin-top': '5vh',
            #        'margin-bottom': '75px',
            #        'margin-left': '75px',
            #        'margin-right': '75px'}
        ),
        html.Img(
            id="ceos-pvp_breakdown_image",
            src="assets/ceos-pvp_breakdown.png",
            style={
                "width": "80vh",
                "margin-left": "25px",
                "margin-top": "25px",
            },
        ),
    ],
)

# how-to box
how_to_contribute_box = dmc.Card(
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
                """We encourage all sensor operators to provide their 
                                 data in an automated manner.  However, to agree protocols the initial mechanism of 
                                 data transfer will be via direct contact with NPL, system developer and operator, 
                                 through completing a form with the required information. To start the process, 
                                 please contact  [*Samantha.Malone@npl.co.uk*](mailto:samantha.malone@npl.co.uk).""",
                style={"text-align": "justify"},
            )
        ),
        html.Div(
            dcc.Markdown(
                """The information that will be required in order to contribute is:""",
                style={"text-align": "justify"},
            )
        ),
        html.Div(
            dcc.Markdown(
                """
                                          - Mission/sensor details (product description/data reader).
                                          - Sensor performance specification.
                                          - Spectral Response Functions (SRFs) for sensors (radiometric aspects) - these will not be made publicly accessible if preferred.""",
                style={"text-align": "left"},
            )
            # style={'margin-top': '5vh',
            #        'margin-bottom': '75px',
            #        'margin-left': '75px',
            #        'margin-right': '75px'}
        ),
    ],
)

# project links box
project_links_box = dmc.Card(
    withBorder=True,
    shadow="xs",
    radius="md",
    children=[
        html.H2(
            "How does the CEOS-PVP fit within other ongoing Cal/Val activities?",
            # style={'margin-top': '5vh',
            #      'margin-left': '75px',
            #      'margin-right': '75px'}
        ),
        # html.P(
        html.Div(
            dcc.Markdown(
                """The RadVAL dashboard is hosted within the UK's national 
                                 Earth Observation Data Hub infrastructure as a service for CEOS and the global EO satellite community.                                                        
                                   """,
                style={"text-align": "justify"},
            )
        ),
        html.Div(dcc.Markdown("""""", style={"text-align": "justify"})),
        html.Div(
            dcc.Markdown("""""", style={"text-align": "left"})
            # style={'margin-top': '5vh',
            #        'margin-bottom': '75px',
            #        'margin-left': '75px',
            #        'margin-right': '75px'}
        ),
    ],
)

# blank content box
blank_content_box = dmc.Card(
    withBorder=True,
    shadow="xs",
    radius="md",
    children=[
        html.H2(
            "Other content",
            # style={'margin-top': '5vh',
            #      'margin-left': '75px',
            #      'margin-right': '75px'}
        ),
        # html.P(
        html.Div(
            dcc.Markdown("""Description.""", style={"text-align": "justify"}),
            # style={'margin-top': '5vh',
            #        'margin-bottom': '75px',
            #        'margin-left': '75px',
            #        'margin-right': '75px'}
        ),
    ],
)

# layout = html.Div([
#     html.H1('This is our CEOS Activity landing page', style={'margin-top': '5vh',
#                                                 'margin-left': '75px',
#                                                 'margin-right': '75px'}),
#     html.Div('This is our CEOS Activity landing page content.', style={'margin-top': '5vh',
#                                                           'margin-bottom': '75px',
#                                                           'margin-left': '75px',
#                                                           'margin-right': '75px'})
# ])

layout = dmc.MantineProvider(
    html.Div(
        [  # dcc.Location(id='page_url', pathname='ceos-activity'),
            dbc.Row(
                dbc.Col(
                    dmc.Container(
                        fluid=True,
                        children=[
                            dbc.Row(
                                children=[
                                    dbc.Col(outline_box),  # xs=2, sm=2, md=2, lg=2,
                                    dbc.Col(
                                        rad_geo_sites_box,  # xs=2, sm=2, md=2, lg=2,
                                        # style={'margin-left': '10px'},
                                    ),
                                ]
                            )
                        ],
                    )
                ),
                style={
                    "margin-top": "0vh",
                    "margin-left": "75px",
                    "margin-right": "75px",
                },
            ),
            dbc.Row(
                dbc.Col(
                    dmc.Container(
                        fluid=True,
                        children=[
                            dbc.Row(
                                children=[
                                    dbc.Col(how_to_contribute_box),
                                    dbc.Col(project_links_box),
                                    dbc.Col(blank_content_box),
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
            # dbc.Row(
            #         dbc.Col(dmc.Container(fluid=True, children=[
            #             dbc.Row(children=[
            #                 dbc.Col(project_links_box),
            #                 dbc.Col(blank_content_box),
            #                 dbc.Col(blank_content_box), # xs=2, sm=2, md=2, lg=2,
            #             ])
            #         ])),
            #     style={'margin-top': '5vh', 'margin-bottom': '5vh',
            #            'margin-left': '75px', 'margin-right': '75px'}, )
        ]
    )
)
