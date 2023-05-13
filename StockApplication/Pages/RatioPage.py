from dash import Dash
from dash import html
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
from dash import html, dcc, Input, Output, ctx, callback
import dash_bootstrap_components as dbc
import dash
import plotly.express as px
import DisplayElementsClass
import GetRatios
import Graphs
import Tables
import json
import pandas as pd
import Callbacks
import APICalls
from Dataprocessing import CreateDataFrames


dash.register_page(__name__)


CreateStaticElement = DisplayElementsClass.MainDisplayElements

sidebar = CreateStaticElement.Create_SideBar()
#TopMenu = CreateStaticElement.Create_FundamentalTopBar('input','SearchStockButton','ShowQuarterly')


#Define Element IDs and names. Build a Matrix consisiting of 13 lists with 6 entries to initalize RatioElements
InitializerList=[]
IDIterator={}
ElementNames= [
"Equity to Asset Ratio Current Quarter: ",
"Debt To Equity to Ratio Current Quarter: ", 
"Long-Term Debt To Equity to Ratio Current Quarter: ",
"Short-Term Debt To Equity to Ratio Current Quarter: ", 
"Fixed Asset Ratio Current Quarter: ",
"Coverage Ratio I Current Quarter: ",
"Coverage Ratio II Current Quarter: ", 
"Cash Ratio Current Quarter: ",
"Quick Ratio Current Quarter: ",
"Current Ratio Current Quarter: ",
"Return On Equity Current Quarter: ", 
"Return On Assets Current Quarter: ", 
"Return On Sales Current Quarter: ",
"Operating Margin: ",
"CashFlow to Revenue Ratio: " ]

z=0
for j in range(1,16):
    ElementList=[]
    for i in range (1,5):
        ElementList.append("{}".format(j)+"x"+"{}".format(i))

    ElementList.append(ElementNames[z])
    z=z+1  

    ElementList.append("{}".format(j)+"x"+"6")
    InitializerList.append(ElementList)

ObjectList = []
ElementList =[]
HeaderList = []
NamingIterator = {}

#Initalize Class-Objects
for x in range(len(InitializerList)):
    Object = DisplayElementsClass.RatioDisplayElements(*InitializerList[x])
    ObjectList.append(Object)

#Create Rationame and Ratio for Current Quarter from Class Objects
for Object in ObjectList:
  Element,Header = Object.CreateRatioElement()
  HeaderList.append(Header)
  ElementList.append(Element)


layout = dbc.Container(html.Div(
                         [
                          sidebar,
                         dbc.Row(
                            # Header Here
                             ),    
                         dbc.Row([
                             dbc.Col(HeaderList[0],width={"size": 3,"offset": 1}),
                             dbc.Col(HeaderList[1],width={"size": 3}),
                             dbc.Col(HeaderList[2],width={"size": 3}),
                             ]),                         
                         dbc.Row([
                             dbc.Col(ElementList[0],width={"size": 3,"offset": 1}),
                             dbc.Col(ElementList[1],width={"size": 3}),
                             dbc.Col(ElementList[2],width={"size": 3}),
                             ]),
                         dbc.Row([
                             dbc.Col(HeaderList[3],width={"size": 3,"offset": 1}),
                             dbc.Col(HeaderList[4],width={"size": 3}),
                             ]), 
                        dbc.Row([
                             dbc.Col(ElementList[3],width={"size": 3,"offset": 1}),
                             dbc.Col(ElementList[4],width={"size": 3}),                           
                            ]),
                         dbc.Row([
                             dbc.Col(HeaderList[5],width={"size": 3,"offset": 1}),
                             dbc.Col(HeaderList[6],width={"size": 3}),
                            ]),
                         dbc.Row([
                             dbc.Col(ElementList[5],width={"size": 3, "offset": 1}),
                             dbc.Col(ElementList[6],width={"size": 3})
                             ]),
                         dbc.Row([
                             dbc.Col(HeaderList[7],width={"size": 3,"offset": 1}),
                             dbc.Col(HeaderList[8],width={"size": 3}),
                             dbc.Col(HeaderList[9],width={"size": 3}),
                         ]),    
                         dbc.Row([
                             dbc.Col(ElementList[7],width={"size": 3, "offset": 1}),
                             dbc.Col(ElementList[8],width={"size": 3}), 
                             dbc.Col(ElementList[9],width={"size": 3}), 
                             ]),
                          dbc.Row([
                             dbc.Col(HeaderList[10],width={"size": 3,"offset": 1}),
                             dbc.Col(HeaderList[11],width={"size": 3}),
                             ],
                             ),    
                          dbc.Row([
                              dbc.Col(ElementList[10],width={"size": 3, "offset": 1}),
                              dbc.Col(ElementList[11],width={"size": 3}), 
                            ]),
                          dbc.Row([
                             dbc.Col(HeaderList[12], width={"size": 3, "offset": 1}),
                             dbc.Col(HeaderList[13], width={"size": 3}),
                             ]),
                          dbc.Row([
                             dbc.Col(ElementList[12], width={"size": 3,"offset": 1}),
                             dbc.Col(ElementList[13], width={"size": 3}),
                          ]),
                          dbc.Row([
                             dbc.Col(HeaderList[14],width={"size": 3,"offset":1}),
                             ]),
                          dbc.Row([
                             dbc.Col(ElementList[14],width={"size": 3,"offset": 1}),
                        ]) ]),
                          fluid=True)

#Callback Elements are Searched in Dataframe
CallbackElements = [["EquityToAssetStateButton",["totalShareholderEquity"], ["totalAssets"], "Equity to Asset Ratio: ", ObjectList[0]],
["DebtEquityStateButton",["totalLiabilities"], ["totalShareholderEquity"], "Debt to Equity Ratio: ",ObjectList[1]],
["LongTermDebtEquityStateButton",["longTermDebt"], ["totalShareholderEquity"], "Long Term Debt to Equity Ratio: ", ObjectList[2]],
["ShortTermDebtEquityStateButton",["shortTermDebt"], ["totalShareholderEquity"], "Short Term Debt to Equity Ratio: ",  ObjectList[3]],
["FixedAssetRatioStateButton",["totalNonCurrentAssets"], ["totalAssets"], "Fixed Asset Ratio: ", ObjectList[4]],
["CoverageRatioIStateButton",["totalShareholderEquity"], ["totalNonCurrentAssets"], "Coverage Ratio I: ", ObjectList[5]],
["CoverageRatioIIStateButton",["totalShareholderEquity","longTermDebt"], ["totalNonCurrentAssets"], "Coverage Ratio II: ",  ObjectList[6]],
["CashRatioStateButton",["cashAndCashEquivalentsAtCarryingValue","cashAndShortTermInvestments"], ["totalCurrentLiabilities"],"Cash Ratio: ",  ObjectList[7]],
["QuickRatioStateButton",["cashAndCashEquivalentsAtCarryingValue","cashAndShortTermInvestments","currentNetReceivables"], ["totalCurrentLiabilities"],"Quick Ratio: ",  ObjectList[8]],
["CurrentRatioStateButton",["totalCurrentAssets"], ["totalCurrentLiabilities"], "Current Ratio: ",  ObjectList[9]],
["RetunOnEquityStateButton",["netIncome"],["totalShareholderEquity"], "Return on Equity: ", ObjectList[10]],
["ReturnOnAssetsStateButton",["netIncome"],["totalAssets"], "Return on Assets: ", ObjectList[11]],
["ReturnOnSalesStateButton",["ebit"],["totalRevenue"], "Return on Sales (EBIT-Margin): ", ObjectList[12]],
["OperatingMarginStateButton",["operatingIncome"],["totalRevenue"], "Operating Margin: ", ObjectList[13]],
["CashFlowToRevenuesStateButton",["operatingCashflow"],["totalRevenue"], "Operating Cashflow to Sales Ratio: ", ObjectList[14]]
]


for x in range(len(CallbackElements)):
    InitCallBack = Callbacks.RatioElement(*CallbackElements[x])
    InitCallBack.RatioCallback()
