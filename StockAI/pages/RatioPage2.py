from dash import Dash
from dash import html
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
from dash import html, dcc, Input, Output, ctx, callback
import dash_bootstrap_components as dbc
import dash
import plotly.express as px
import GetRatios
import Graphs
import Tables
import pandas as pd
import Callbacks
import DisplayElementsClass


dash.register_page(__name__)

CreateMainElement = DisplayElementsClass.MainDisplayElements

sidebar = CreateMainElement.Create_SideBar()
#TopMenu = CreateMainElement.Create_FundamentalTopBar('inputSM','SearchStockButtonSM','ShowQuarterlySM')

#TopMenu = CreateStaticElement.Create_FundamentalTopBar('input','SearchStockButton','ShowQuarterly')


#Define Element IDs and names. Build a Matrix consisiting of 13 lists with 6 entries to initalize RatioElements
InitializerList=[]

ElementNames= [
"Earnings Per Share Current Quarter: ",
"Price Earnings Ratio Current Quarter: "
]

z=0
for j in range(18,20):
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


Earnings_Per_Share_Header, Price_To_Earnings_Header = [i for i in HeaderList]

Earnings_Per_Share_Element, Price_To_Earnings_Element,= [i for i in ElementList]


layout = dbc.Container(html.Div(
                         [
                         sidebar,
                         dbc.Row(
                             ),    
                          dbc.Row([
                             dbc.Col(Earnings_Per_Share_Header,width={"size": 3,"offset":1}),
                             dbc.Col(Price_To_Earnings_Header,width={"size": 3}),

                             ]),
                          dbc.Row([
                             dbc.Col(Earnings_Per_Share_Element,width={"size": 3,"offset": 1}),
                             dbc.Col(Price_To_Earnings_Element,width={"size": 3}),

                        ]) ]),
                          fluid=True)


CallbackElements = [["EPSStateButton","Earnings per Share: ", ObjectList[0] ,"Multiple","$","","$",".2f"],
["PriceEarningsStateButton","Price Earnings Ratio: ",ObjectList[1],"Multiple","","","",".1f"]]

for x in range(len(CallbackElements)):
    InitCallBack = Callbacks.RatioElementSpecial(*CallbackElements[x])
    InitCallBack.RatioCallback()
