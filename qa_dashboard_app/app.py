import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from logging import Logger


# create app
app = Dash(
    __name__,
    # suppress_callback_exceptions=True,
    use_pages=True,
    external_stylesheets=[dbc.themes.SIMPLEX, dbc.icons.BOOTSTRAP],
    title='CEOS Calibration Dashboard'
)

application = app.server

HEIGHT_OF_ROW = 345

log = Logger(__name__)

# add upper buttons based on pages
page_buttons = dbc.Container(fluid='xs',
                             style={'width': '110vh',
                                                # 'margin-left': '1px',
                                                'margin-right': '3vh'
                                                },
                             children=[
                                 html.Div([dbc.Row(
                                     children=[
                                         dbc.Col(
                                             html.Div(dbc.ButtonGroup([
                                                 dbc.Button(f"{page['name']}", href=page["relative_path"],  # - {page['path']}
                                                            size='lg', color='dark',
                                                            style={'color': 'rgb(150, 150, 255)', 'width': '160px', #' height': '250px',
                                                                   'verticalAlign': 'middle',
                                                                   # 'margin-left': '-10vh'
                                                                   },
                                                            outline=True)])),
                                         style={ 'padding': '2px'}) for page in dash.page_registry.values() if page["location"] == "sidebar"
                                     ],
                                     style = {'width': 'auto'}
                                 )
                                 ])
                             ])

# create header of logos and buttons
header = dmc.Card(
    children=[
        dbc.Container(fluid='xs',
                      # style={'margin-bottom': '5vh',
                      #              'margin-left': '5vh'},
                      children=[
                          dbc.Row(
                              children=[
                                  dbc.Col(dbc.Container(fluid='xs',
                                                        style={'margin-left': '0vh', 'margin-top': '0vh'},
                                                        children=[
                                                            html.A(
                                                                href="https://ceos.org/", target='newPage',  # https://calvalportal.ceos.org/web/guest
                                                                children=[
                                                                    html.Img(
                                                                        alt="Link to CEOS portal",
                                                                        src="assets/CEOS_logo_colour_no_text.png",
                                                                        height=75
                                                                    )
                                                                ]
                                                            )
                                                            # width=100),
                                                        ])),
                                  dbc.Col(dbc.Container(fluid='xs',
                                                        style={'width': '20vh',
                                                               'margin-top': '0vh', 'margin-left': '-5vh'},
                                                        children=[
                                                            dmc.Text("Calibration Dashboard",
                                                                     weight=500, align="left", inline=True,
                                                                     style={'font-size': '2rem',
                                                                            'font-family': 'Segoe UI',
                                                                            # 'position': 'absolute',
                                                                            'top': '12',
                                                                            })])),
                                  dbc.Col(page_buttons, style={'margin-top': '1vh', 'margin-right': '1vh'})
                              ])

                      ])])

# create footer of logos & links
footer = dmc.Card(
    children=[
        dbc.Container(fluid=True, children=[
            dbc.Row([
                dbc.Col(
                    html.A(
                        href="https://ceos.org/", target='newPage',  # https://calvalportal.ceos.org/web/guest
                        children=[
                            html.Img(
                                alt="Link to CEOS portal",
                                src="assets/CEOS_logo_colour_no_text.png",
                                height=90
                            )
                        ]
                    ), align="center"
                ),
                dbc.Col(width={"size": 4, }, #"offset": 2},
                        children=[
                            html.Div(children=[
                                dcc.Link('Committee on Earth Observation Satellites',
                                         href='https://www.ceos.org/', target='newPage'),
                            ]),
                            html.Div(children=[
                                dcc.Link('Working Group Calibration and Validation',
                                         href='https://ceos.org/ourwork/workinggroups/wgcv/', target='newPage'),
                            ]),
                            html.Div(children=[
                                dcc.Link(' Privacy Policy |', href='', target='newPage'),
                                dcc.Link(' Disclaimer |', href='', target='newPage'),
                                dcc.Link(' Accessibility', href='', target='newPage')
                            ])
                        ]),
                dbc.Col(
                    html.A(
                        href="https://staging.eodatahub.org.uk/", target='newPage',
                        children=[
                            html.Img(
                                alt="Link to EODH",
                                src="assets/powered_by_eodh.png",
                                height=100
                            )
                        ]
                    ), align="center")
                ,
                dbc.Col(
                    html.A(
                        href="https://www.npl.co.uk/", target='newPage',
                        children=[
                            html.Img(
                                alt="Link to NPL",
                                src="assets/NPL_logo_blue.png",
                                height=75
                            )
                        ]
                    ), align="center")
                ,
                dbc.Row([html.Div([html.Br()])]),  # add in empty row for spacing
                dbc.Row([dbc.Col(
                    html.Div('Version 1.1'),
                    style={'font-size': '1.1rem'},
                    width={"order": "last", "offset": 10},
                )
                ])
            ])
        ])
    ])


app.layout = html.Div([
    dbc.Row(children=[
        dbc.Container(fluid=True, children=[
            dbc.Col(header, style={'margin-bottom': '5vh',
                                   'margin-left': '5vh',
                                   'margin-right': '5vh'}),  # , xs=12, sm=12, md=12, lg=12)),
        ])]),
    dash.page_container,
    dbc.Row(
        dbc.Col(footer, style={'margin-bottom': '5vh',
                               'margin-left': '5vh'})  # xs=12, sm=12, md=12, lg=12))
    )
])

if __name__ == '__main__':
    app.run(debug=True,  # for testing locally
            # dev_tools_ui=False, dev_tools_props_check=False  # disables the blue marker that shows errors
            )
    # app.run(debug=False, host='0.0.0.0', port=5000)  # for running in Docker container
