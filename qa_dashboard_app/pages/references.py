import dash
from dash import html, dcc, callback, Input, Output

dash.register_page(__name__,
                   order=5,
                   title='Calibration Dashboard - References',  # name of tab
                   # image='references.png',
                   description='Reference information.',
                   location="sidebar")

HEIGHT_OF_ROW = 345

layout = html.Div([
    html.H1('This is our References page', style={'margin-top': '5vh',
                                                  'margin-left': '75px',
                                                  'margin-right': '75px'}),
    html.Div('This is our References page content.', style={'margin-top': '5vh',
                                                            'margin-bottom': '75px',
                                                            'margin-left': '75px',
                                                            'margin-right': '75px'})
])
