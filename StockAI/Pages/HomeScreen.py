from dash import html
import dash
from DisplayElementsClass import MainDisplayElements

dash.register_page(__name__, path='/')

CreateMainElement = MainDisplayElements

sidebar = CreateMainElement.Create_SideBar()


layout = html.Div([sidebar])
