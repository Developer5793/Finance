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
"Return on Sales Ratio Current Quarter: ",
"Operating Profit Margin Current Quarter: ",
"Profit Margin Ratio Current Quarter: ",
"Interest Coverage Ratio Current Quarter: ",
"CashFlow to Revenue Ratio Current Quarter: ",
]

z=0
for j in range(1,18):
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

#Initalize Class-Objects
for x in range(len(InitializerList)):
    Object = DisplayElementsClass.RatioDisplayElements(*InitializerList[x])
    ObjectList.append(Object)

#Create Rationame and Ratio for Current Quarter from Class Objects
for Object in ObjectList:
  Element,Header = Object.CreateRatioElement()
  HeaderList.append(Header)
  ElementList.append(Element)


Equity_to_Asset_Header, Debt_to_Equity_Header, Long_Term_Debt_To_Equity_Header,Short_Term_Debt_To_Equity_Header,Fixed_Asset_Header, Coverage_Ratio_I_Header, Coverage_Ratio_II_Header, Cash_Ratio_Header,Quick_Ratio_Header, Current_Ratio_Header, Return_On_Equity_Header, Return_On_Assets_Header, Return_On_Sales_Header, Operating_Profit_Margin_Header, Profit_Margin_Header,Interest_Coverage_Ratio_Header, CashFlow_To_Revenue_Ratio_Header = [i for i in HeaderList]
Equity_to_Asset_Element, Debt_to_Equity_Element, Long_Term_Debt_To_Equity_Element,Short_Term_Debt_To_Equity_Element,Fixed_Asset_Element, Coverage_Ratio_I_Element, Coverage_Ratio_II_Element, Cash_Ratio_Element,Quick_Ratio_Element, Current_Ratio_Element, Return_On_Equity_Element, Return_On_Assets_Element, Return_On_Sales_Element, Operating_Profit_Margin_Element, Profit_Margin_Element,Interest_Coverage_Ratio_Element, CashFlow_To_Revenue_Ratio_Element= [i for i in ElementList]

###for x in mytuple:


layout = dbc.Container(html.Div(
                         [
                         sidebar,
                         dbc.Row(
                             ),    
                         dbc.Row([
                             dbc.Col(Equity_to_Asset_Header,width={"size": 3,"offset": 1}),
                             dbc.Col(Debt_to_Equity_Header,width={"size": 3}),
                             dbc.Col(Long_Term_Debt_To_Equity_Header,width={"size": 3}),
                             ]),                         
                         dbc.Row([
                             dbc.Col(Equity_to_Asset_Element,width={"size": 3,"offset": 1}),
                             dbc.Col(Debt_to_Equity_Element,width={"size": 3}),
                             dbc.Col(Long_Term_Debt_To_Equity_Element,width={"size": 3}),
                             ]),
                         dbc.Row([
                             dbc.Col(Short_Term_Debt_To_Equity_Header,width={"size": 3,"offset": 1}),
                             dbc.Col(Fixed_Asset_Header,width={"size": 3}),
                             ]), 
                        dbc.Row([
                             dbc.Col(Short_Term_Debt_To_Equity_Element,width={"size": 3,"offset": 1}),
                             dbc.Col(Fixed_Asset_Element,width={"size": 3}),                           
                            ]),
                         dbc.Row([
                             dbc.Col(Coverage_Ratio_I_Header,width={"size": 3,"offset": 1}),
                             dbc.Col(Coverage_Ratio_II_Header,width={"size": 3}),
                            ]),
                         dbc.Row([
                             dbc.Col(Coverage_Ratio_I_Element,width={"size": 3, "offset": 1}),
                             dbc.Col(Coverage_Ratio_II_Element,width={"size": 3})
                             ]),
                         dbc.Row([
                             dbc.Col(Cash_Ratio_Header,width={"size": 3,"offset": 1}),
                             dbc.Col(Quick_Ratio_Header,width={"size": 3}),
                             dbc.Col(Current_Ratio_Header,width={"size": 3}),
                         ]),    
                         dbc.Row([
                             dbc.Col(Cash_Ratio_Element,width={"size": 3, "offset": 1}),
                             dbc.Col(Quick_Ratio_Element,width={"size": 3}), 
                             dbc.Col(Current_Ratio_Element,width={"size": 3}), 
                             ]),
                          dbc.Row([
                             dbc.Col(Return_On_Equity_Header,width={"size": 3,"offset": 1}),
                             dbc.Col(Return_On_Assets_Header,width={"size": 3}),
                             ],
                             ),    
                          dbc.Row([
                              dbc.Col(Return_On_Equity_Element,width={"size": 3, "offset": 1}),
                              dbc.Col(Return_On_Assets_Element,width={"size": 3}), 
                            ]),
                          dbc.Row([
                             dbc.Col(Return_On_Sales_Header, width={"size": 3, "offset": 1}),
                             dbc.Col(Operating_Profit_Margin_Header, width={"size": 3}),
                             dbc.Col(Profit_Margin_Header, width={"size": 3}),

                             ]),
                          dbc.Row([
                             dbc.Col(Return_On_Sales_Element, width={"size": 3,"offset": 1}),
                             dbc.Col(Operating_Profit_Margin_Element, width={"size": 3}),
                             dbc.Col(Profit_Margin_Element,width={"size": 3}),

                          ]),
                          dbc.Row([
                             dbc.Col(Interest_Coverage_Ratio_Header,width={"size": 3,"offset":1}),
                             dbc.Col(CashFlow_To_Revenue_Ratio_Header,width={"size": 3}),

                             ]),
                          dbc.Row([
                             dbc.Col(Interest_Coverage_Ratio_Element,width={"size": 3,"offset": 1}),
                             dbc.Col(CashFlow_To_Revenue_Ratio_Element,width={"size": 3}),

                        ]) ]),
                          fluid=True)

#Callback Elements are Searched in Dataframe
CallbackElements = [["EquityToAssetStateButton","Equity to Asset Ratio: ", ObjectList[0]],
["DebtEquityStateButton", "Debt to Equity Ratio: ",ObjectList[1]],
["LongTermDebtEquityStateButton", "Long Term Debt to Equity Ratio: ", ObjectList[2]],
["ShortTermDebtEquityStateButton","Short Term Debt to Equity Ratio: ",  ObjectList[3]],
["FixedAssetRatioStateButton", "Fixed Asset Ratio: ", ObjectList[4]],
["CoverageRatioIStateButton","Coverage Ratio I: ", ObjectList[5]],
["CoverageRatioIIStateButton", "Coverage Ratio II: ",  ObjectList[6]],
["CashRatioStateButton","Cash Ratio: ",  ObjectList[7]],
["QuickRatioStateButton","Quick Ratio: ",  ObjectList[8]],
["CurrentRatioStateButton", "Current Ratio: ",  ObjectList[9]],
["RetunOnEquityStateButton", "Return on Equity: ", ObjectList[10]],
["ReturnOnAssetsStateButton", "Return on Assets: ", ObjectList[11]],
["ReturnOnSalesStateButton", "Return on Sales (EBIT-Margin): ", ObjectList[12]],
["OperatingProfitMarginStateButton","Operating Profit Margin: ", ObjectList[13]],
["ProfitMarginStateButton", "Profit Margin: ", ObjectList[14]],
["InterestCoverageRatioStateButton", "Interest Coverage Ratio: ", ObjectList[15]],
["CashFlowToRevenuesStateButton", "Operating Cashflow to Sales Ratio: ", ObjectList[16]
 ]
]

for x in range(len(CallbackElements)):
    InitCallBack = Callbacks.RatioElement(*CallbackElements[x])
    InitCallBack.RatioCallback()
