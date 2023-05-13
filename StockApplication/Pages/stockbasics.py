from dash.exceptions import PreventUpdate
from dash import html, dcc, Input, Output, ctx, callback, Dash, State
import dash_bootstrap_components as dbc
import dash
import DisplayElementsClass
import pandas as pd
import APICalls
from Dataprocessing import CreateDataFrames
import Tables
import json
from dash import dash_table
import Graphs
import dash_ag_grid as dag
import dash_mantine_components as dmc




dash.register_page(__name__)


CreateStaticElement = DisplayElementsClass.MainDisplayElements

sidebar = CreateStaticElement.Create_SideBar()
#TopMenu = CreateStaticElement.Create_FundamentalTopBar('inputsss','SearchStockButtonss','ShowQuarterlyssss')

CompanyName = html.H3(id="CompanyName")
CompanySymbol = html.H4(id="CompanySymbol")
Description = html.H4(id="Description")


columnDefs =[
    {"headerName":"Statistic Name",
     "field": "NAME"},

   {"headerName":"Value",
     "field": "VALUE"}]

defaultColDef = {
    "resizable": False,
    "sortable": False,
    "editable": False}

GeneralGrid= dag.AgGrid(
            id="GeneralInformation",
            columnDefs=columnDefs,
            className="ag-theme-alpine-dark color-fonts",
            rowData=[],
            columnSize="sizeToFit",
            defaultColDef=defaultColDef,
            dashGridOptions={#"rowSelection": "single",
                            # "rowHeight": 30,
                             "domLayout":'autoHeight'})
OverviewGrid= dag.AgGrid(
            id="OverviewGrid",
            columnDefs=columnDefs,
            className="ag-theme-alpine-dark color-fonts",
            rowData=[],
            columnSize="sizeToFit",
            defaultColDef=defaultColDef,
            dashGridOptions={"rowSelection": "single",
                             "rowHeight": 30,
                             "domLayout":'autoHeight'})



Graph = html.Div(id="StockGraph")


tabs_styles = {
    'height': '44px',
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold',
    'backgroundColor': 'black',
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px'
}

Tabs = html.Div([
    dcc.Tabs(id="tabs-inline", value='tab-6', children=[
        dcc.Tab(label='1 Month', value='tab-1', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='6 Month', value='tab-2', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='1 Year', value='tab-3', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='3 Years', value='tab-4', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='5 Years', value='tab-5', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Max', value='tab-6', style=tab_style, selected_style=tab_selected_style),
    ], style = tabs_styles),

html.Div(id='tabs-content-inline-3')])

layout = dbc.Container(html.Div(
                         [
                         #TopMenu,
                          sidebar,    
                          dbc.Row(
                             dbc.Col(CompanyName,width={"size": 6 , "offset":1})),
                          dbc.Row(
                             dbc.Col(CompanySymbol,width={"size": 6 , "offset":1})),
                          dbc.Row(
                             dbc.Col(Graph,width={"size": 6 , "offset":1})),
                             html.Br(),
                          dbc.Row(
                             dbc.Col(Tabs,width={"size": 6 , "offset":1})),
                             html.Br(),
                          dbc.Row(
                             dbc.Col(GeneralGrid,width={"size": 6 , "offset":1})),
                          dbc.Row(
                             dbc.Col(Description,width={"size": 6 , "offset":1})),
                          dbc.Row(
                             dbc.Col(OverviewGrid,width={"size": 6 , "offset":1})),                   
                          ]),
                          fluid=True)


@callback(
    Output("StockGraph","children"),
    Input("WeeklyPriceInformation","modified_timestamp"),
    State("WeeklyPriceInformation","data"))

def CreateChart(ts, WeeklyPriceInformation):
 if ts is None or WeeklyPriceInformation is None:
       raise PreventUpdate
 GraphObject = Graphs.DrawGraphs

 WeeklyDataFrame =  CreateDataFrames.CreateWeeklyChart(WeeklyPriceInformation)
 WeeklyStockGraph = GraphObject.DrawChart(WeeklyDataFrame)
 return WeeklyStockGraph  

#Create Companyoverview Dataframes
@callback(
    Output("CompanyName", "children"),
    Output("CompanySymbol", "children"),
    Output("Description", "children"),
    Output("GeneralInformation", "rowData"),
    Output("OverviewGrid", "rowData"), 

    Input ("CompanyOverview", "modified_timestamp"),
    State("CompanyOverview","data"), prevent_inital_call=True)

#Create Dataframe with search Results and fill table
def CreateDataTables (ts, CompanyOverviewData):
   if ts is None or CompanyOverviewData is None:
       raise PreventUpdate

   CompanyName, CompanySymbol, CompanyDescription, CompanyOverviewFrame = CreateDataFrames.CreateCompanyOverviewData(CompanyOverviewData)
   CompanyOverviewFrameHumanReadable = CreateDataFrames.MakeDataFrameHumandReadable(CompanyOverviewFrame,["MarketCapitalization","EBITDA","RevenueTTM","GrossProfitTTM","SharesOutstanding"])
   TableObject = Tables.Table(CompanyOverviewFrameHumanReadable)
   GeneralInformationTable = TableObject.CreateOverviewTableDataFrame(["AssetType","FiscalYearEnd","LatestQuarter"])
   OverviewData = TableObject.CreateOverviewTableDataFrame(["MarketCapitalization","EBITDA","PERatio","PEGRatio","DividendPerShare","DividendYield","EPS","RevenuePerShareTTM","ProfitMargin","OperatingMarginTTM","ReturnOnAssetsTTM","ReturnOnEquityTTM","RevenueTTM","GrossProfitTTM","DilutedEPSTTM","QuarterlyEarningsGrowthYOY","QuarterlyRevenueGrowthYOY","AnalystTargetPrice","TrailingPE","ForwardPE","PriceToSalesRatioTTM","PriceToBookRatio","EVToRevenue","EVToEBITDA"])

   return CompanyName, CompanySymbol, CompanyDescription, GeneralInformationTable, OverviewData


@callback(Output('StockGraph', 'children', allow_duplicate=True),
          Input('tabs-inline', 'value'),
          Input("WeeklyPriceInformation","modified_timestamp"),
          State("WeeklyPriceInformation","data"),prevent_initial_call=True) 

def render_content(tab, ts, WeeklyPriceInformation):
    if ts is None:
        raise PreventUpdate

    if tab == 'tab-1':
        return 
    elif tab == 'tab-2':
        return html.Div([
            html.H3('Tab content 2')
        ])
    elif tab == 'tab-3':
        return html.Div([
            html.H3('Tab content 3')
        ])
    elif tab == 'tab-4':
     GraphObject = Graphs.DrawGraphs
     WeeklyDataFrame =  CreateDataFrames.CreateWeeklyChart(WeeklyPriceInformation)
     WeeklyStockGraph = GraphObject.DrawChart(WeeklyDataFrame)
     return WeeklyStockGraph  

    elif tab == 'tab-5':
        return html.Div([
            html.H3('Tab content 3')
        ])

    elif tab == 'tab-6':
        return html.Div([
            html.H3('Tab content 3')
        ])








