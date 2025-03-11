import dash
from dash import html

dash.register_page(__name__,
                   order=7,
                   title='Click a button to return to the app',  # name of tab
                   description='404',
                   location="None")

HEIGHT_OF_ROW = 345

layout = html.H2("Please click Dashboard to return to Dashboard homepage.",
                 style={'margin-top': '5vh',
                        'margin-bottom': '75px',
                        'margin-left': '75px',
                        'margin-right': '75px'}
                 )
