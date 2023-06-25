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

GeneralGrid= html.Div(dag.AgGrid(
            id="GeneralInformation",
            columnDefs=columnDefs,
            className="ag-theme-alpine-dark color-fonts",
            rowData=[],
            columnSize="sizeToFit",
            defaultColDef=defaultColDef,
            dashGridOptions={
                             "domLayout":'autoHeight'}),
            style={

                        "height": "250px",
                        'overflow': 'hidden'})   
            



NumerizedGrid= html.Div(dag.AgGrid(
            id="NumerizedGrid",
            columnDefs=columnDefs,
            className="ag-theme-alpine-dark color-fonts",
            rowData=[],
            columnSize="sizeToFit",
            defaultColDef=defaultColDef,
            dashGridOptions={"rowSelection": "single",
                             "domLayout":'autoHeight'}), style={

                        "height": "340px",
                        'overflow': 'hidden'})   

StockRatioGrid= html.Div(dag.AgGrid(
            id="StockRatioGrid",
            columnDefs=columnDefs,
            className="ag-theme-alpine-dark color-fonts",
            rowData=[],
            columnSize="sizeToFit",
            defaultColDef=defaultColDef,
            dashGridOptions={"rowSelection": "single",
                             "domLayout":'autoHeight'}), 
                         style={ 
                             
                        "height": "595px",
                        'overflow': 'hidden'})   


CompanyRatioGrid= html.Div(dag.AgGrid(
            id="CompanyRatioGrid",
            columnDefs=columnDefs,
            className="ag-theme-alpine-dark color-fonts",
            rowData=[],
            columnSize="sizeToFit",
            defaultColDef=defaultColDef,
            dashGridOptions={"rowSelection": "single",               
                        "domLayout":'autoHeight'}),  
              style={       
                        "height": "auto",                   
                        'overflow': 'hidden'})   



Graph = html.Div(id="StockGraph", style={

                        "height": "425px",
                        'overflow': 'hidden'})       



Tabs = dbc.Tabs([
        dbc.Tab(label='1 Month', tab_id='tab-1', className="mt-3"),
        dbc.Tab(label='6 Month', tab_id='tab-2', className="mt-3"),
        dbc.Tab(label='1 Year', tab_id='tab-3', className="mt-3"),
        dbc.Tab(label='3 Years', tab_id='tab-4', className="mt-3"),
        dbc.Tab(label='5 Years', tab_id='tab-5', className="mt-3"),
        dbc.Tab(label='Max', tab_id='tab-6', className="mt-3"),
    ],    id="tabs",
          active_tab="tab-1",
    )


layout = dbc.Container(html.Div(
                         [
                         #TopMenu,
                          sidebar,    
                          dbc.Row(
                             dbc.Col(html.Div(CompanyName),width={"size": 6 , "offset":1})),
                          dbc.Row(
                             dbc.Col(html.Div(CompanySymbol),width={"size": 6 , "offset":1})),
                          dbc.Row(
                            dbc.Col(html.Div(Tabs),width={"size": 6 , "offset":1})),
                         dbc.Row(
                            dbc.Col(Graph,width={"size": 6 , "offset":1})),
                         dbc.Row(
                             dbc.Col(html.Div(GeneralGrid),width={"size": 6 , "offset":1})),                  
                          dbc.Row(
                             dbc.Col(html.Div(NumerizedGrid),width={"size": 6 , "offset":1})),                    
                          dbc.Row(
                             dbc.Col(html.Div(StockRatioGrid),width={"size": 6 , "offset":1})),                      
                          dbc.Row(
                             dbc.Col(html.Div(CompanyRatioGrid),width={"size": 6 , "offset":1})),                      
                          dbc.Row(
                             dbc.Col(html.Div(Description),width={"size": 6 , "offset":1})),

                          ]),
                          fluid=True)


@callback(
    Output("StockGraph","children"),
    Input("MonthlyPriceInformation","modified_timestamp"),
    State("MonthlyPriceInformation","data"))

def CreateChart(ts, MonthlyPriceInformation):
 if ts is None or MonthlyPriceInformation is None:
       raise PreventUpdate
 GraphObject = Graphs.DrawGraphs

 MonthlyDataFrame =  CreateDataFrames.CreatePriceDataFrame(MonthlyPriceInformation,"Monthly Adjusted Time Series")
 WeeklyStockGraph = GraphObject.DrawChart(MonthlyDataFrame)
 return WeeklyStockGraph  

#Create Companyoverview Dataframes
@callback(
    Output("CompanyName", "children"),
    Output("CompanySymbol", "children"),
    Output("Description", "children"),
    Output("GeneralInformation", "rowData"),
    Output("NumerizedGrid", "rowData"), 
    Output("StockRatioGrid", "rowData"), 
    Output("CompanyRatioGrid", "rowData"), 


    Input ("CompanyOverview", "modified_timestamp"),
    State("CompanyOverview","data"))

#Create Dataframe with search Results and fill table
def CreateDataTables (ts, CompanyOverviewData):
   if ts is None or CompanyOverviewData is None:
       raise PreventUpdate

   CompanyName, CompanySymbol, CompanyDescription, CompanyOverviewFrame = CreateDataFrames.CreateCompanyOverviewData(CompanyOverviewData)
   CompanyOverviewFrameHumanReadable = CreateDataFrames.MakeDataFrameHumandReadable(CompanyOverviewFrame,["MarketCapitalization","EBITDA","RevenueTTM","GrossProfitTTM","SharesOutstanding"])
   TableObject = Tables.Table(CompanyOverviewFrameHumanReadable)
   GeneralInformationTable = TableObject.CreateOverviewTableDataFrame(["AssetType","FiscalYearEnd","LatestQuarter","SharesOutstanding"])
   NumerizedData = TableObject.CreateOverviewTableDataFrame(["MarketCapitalization","EBITDA","RevenueTTM","GrossProfitTTM","EVToRevenue","EVToEBITDA"])
   StockRatioGrid = TableObject.CreateOverviewTableDataFrame(["PERatio","PEGRatio","EPS","RevenuePerShareTTM","GrossProfitTTM","DilutedEPSTTM","TrailingPE","ForwardPE","PriceToSalesRatioTTM","PriceToBookRatio","DividendPerShare","DividendYield"])
   CompanyRatioGrid =TableObject.CreateOverviewTableDataFrame(["ProfitMargin","OperatingMarginTTM","ReturnOnAssetsTTM","ReturnOnEquityTTM"])
   #"PERatio","PEGRatio","DividendPerShare","DividendYield","EPS","RevenuePerShareTTM","ProfitMargin","OperatingMarginTTM","ReturnOnAssetsTTM","ReturnOnEquityTTM","RevenueTTM","GrossProfitTTM","DilutedEPSTTM","QuarterlyEarningsGrowthYOY","QuarterlyRevenueGrowthYOY","AnalystTargetPrice","TrailingPE","ForwardPE","PriceToSalesRatioTTM","PriceToBookRatio","EVToRevenue","EVToEBITDA"])

   return CompanyName, CompanySymbol, CompanyDescription, GeneralInformationTable, NumerizedData, StockRatioGrid, CompanyRatioGrid


@callback(Output('StockGraph', 'children', allow_duplicate=True),
          Input('tabs', 'active_tab'),
          Input("MonthlyPriceInformation","modified_timestamp"),
          State("MonthlyPriceInformation","data"),prevent_initial_call=True) 

def render_content(tab, ts, MonthlyPriceInformation):
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
     WeeklyDataFrame =  CreateDataFrames.CreatePriceDataFrame(MonthlyPriceInformation,"Monthly Adjusted Time Series")
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








