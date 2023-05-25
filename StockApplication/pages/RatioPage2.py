from dash import Dash
from dash import html
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
from dash import html, dcc, Input, Output, ctx, callback
import dash_bootstrap_components as dbc
import dash
import plotly.express as px
from DisplayElementsClass import MainDisplayElements
import GetRatios
import Graphs
import Tables
import pandas as pd
import Callbacks


dash.register_page(__name__)

CreateMainElement = MainDisplayElements

sidebar = CreateMainElement.Create_SideBar()
#TopMenu = CreateMainElement.Create_FundamentalTopBar('inputSM','SearchStockButtonSM','ShowQuarterlySM')


layout=[sidebar]



