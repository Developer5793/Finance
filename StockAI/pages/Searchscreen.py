from sqlite3 import DatabaseError
from dash.exceptions import PreventUpdate
from dash import html, dcc, Input, Output, callback, Dash, State
import dash_bootstrap_components as dbc
import dash
from DisplayElementsClass import MainDisplayElements
import pandas as pd
import APICalls
import Dataprocessing
import Tables
import Graphs
import dash_ag_grid as dag
import dash_mantine_components as dmc
import pandas as pd
from dash_iconify import DashIconify
import numpy as np
from GetRatios import Ratios

dash.register_page(__name__)

CreateMainElement = MainDisplayElements

sidebar = CreateMainElement.Create_SideBar()

StockSearchInput = dbc.Input(id="SearchStockInput", placeholder="Enter Stock please", type='text', minLength="800", debounce=True)
SearchStockButton = dbc.Button("Search",id ="SearchBtn",size="sm",outline="True", color="primary",style={"width":"80px", "marginLeft": "5px"},className="me-2"),

data = {'SYMBOL': ['GOOG', 'MSFT', 'META', 'NFLX', 'AAPL',"TSLA","AMZN","GME","AMD","PYPL"],
        'NAME': ["Alphabet Inc.", "Microsoft Corporation", "Meta Platforms Inc.", "Netflix Inc.", "Apple Inc.", "TSLA.Inc", "Amazon.com Inc.", "GameStop", "Advanced Micro Devices Inc.", "PayPal"],
        }

DefaultSearchTableDf = pd.DataFrame(data)
DefaultSearchTableDf['REGION']="United States"
DefaultSearchTableDf['CURRENCY']="USD"
DefaultSearchTableDf['GRAPH']=""

SQLPricecharts =APICalls.SQLQueries("StockPricesSearchTable")
Prices= SQLPricecharts.CreateSQLTable()
GraphObject = Graphs.DrawGraphs


for index, row in DefaultSearchTableDf.iterrows():
  PriceDataFrame = Prices.loc[Prices['Tag'] == row["SYMBOL"]]
  PriceDataFrame.reset_index(drop=True, inplace=True)
  PriceDataFrame = PriceDataFrame.iloc[:53]
  Graph = GraphObject.DrawTableChart(PriceDataFrame)
  DefaultSearchTableDf.at[index, 'GRAPH'] = Graph

columnDefs =[

    {"headerName":"Stock Ticker",
     "field": "SYMBOL",
     "sortable": True, 
     "filter": True,
     "cellRenderer": "DMC_Button",
     "maxWidth": 175,
     "minWidth": 175,
     "cellRendererParams": {
        "rightIcon": "ph:eye",
        "style": {
                "margin": "5px",
                "display": 'flex',
                "justifyContent": 'center',
                "alignItems": 'center',
                "maxWidth": 100,
                "minWidth": 100,
            }
        },
     },
 
    {"headerName": "TTM",
     "field":"GRAPH", 
     "cellRenderer": "DCC_GraphClickData", 
     "maxWidth": 175,
     "minWidth": 175,
    },

    {"headerName":"Company Name",
     "field": "NAME",
     "sortable": True, 
     "filter": True,
     'cellStyle':{
        "display": "flex",
        "vertical-align": "middle",
        "align-items": "center"} 
      },

    {"headerName": "Region",
      "field": "REGION",
      "sortable": True, 
      "filter": True,
      'cellStyle':{
        "display": "flex",
        "vertical-align": "middle",
        "align-items": "center" }
      },

    {"headerName": "Currency",
     "field": "CURRENCY",
     'cellStyle':{
        "display": "flex",
        "vertical-align": "middle",
        "align-items": "center"}
     }
]

defaultColDef = {
    "resizable": True,
    "sortable": False,
    "editable": False,
}
grid= dag.AgGrid(
            id="selection-single-grid",
            columnDefs=columnDefs,
            className="ag-theme-alpine-dark color-fonts",
            rowData=DefaultSearchTableDf.to_dict('records'),
            columnSize="sizeToFit",
            defaultColDef=defaultColDef,
            dashGridOptions={"rowSelection": "single",
                             "rowHeight": 60,
                             "domLayout":'autoHeight'}
            )


layout = dbc.Container(
                 html.Div
                    (
                 [
                     sidebar,
                 dbc.Row([
                     dbc.Col(StockSearchInput, width={"size": 6 , "offset": 1}),
                     dbc.Col(SearchStockButton, width={"size": 2})
                     ]),   
                 html.Br(),  
                 dbc.Row([
                     dbc.Col(grid, width={"size": 9 , "offset": 1})]),
                 
				 #Stores for Searchscreen
				 dcc.Store(id="SearchResults",storage_type='memory'),
		         dcc.Location(id='location'),
                    ]), fluid=True
                 )


@callback(
    Output("SearchResults", "data"),
    Input("SearchBtn", "n_clicks"),
    State("SearchStockInput", "value"),prevent_initial_call=True)
def EnterStock(n_clicks, search_value):
    if n_clicks is None or search_value is None:
        raise PreventUpdate

    SearchObject = APICalls.APIRequests
    SearchResults = SearchObject.SearchEndpoint(search_value)
    DataObject = Dataprocessing.CreateDataFrames 
    SearchResultFrame = DataObject.CreateSearchResultDataFrame(SearchResults)

    return SearchResultFrame

@callback(
    Output("selection-single-grid", "rowData", allow_duplicate=True),
    Input ("SearchResults", "modified_timestamp"),
    State("SearchResults","data"), prevent_initial_call=True)

##Create Dataframe with search Results and fill table
def FillTableWSithSearchResults (ts, FilteredStocks):
   if ts is None or FilteredStocks is None:
       raise PreventUpdate
   TableObject = Tables.Table(FilteredStocks)
   SearchObject = APICalls.APIRequests
   DataObject = Dataprocessing.CreateDataFrames
   GraphObject = Graphs.DrawGraphs

   SearchResults = TableObject.CreateSearchTableDataFrame()
   ##Create Graphs for Search Results
   for index, row in SearchResults.iterrows():

    StockPriceChart = SearchObject.ReceivePriceInformation("WEEKLY",row["SYMBOL"])
    #PriceDataFrame = DataObject.CreateWeeklyChart(StockPriceChart)
    ###Here max 52 rows
    Graph = GraphObject.DrawTableChart(PriceDataFrame)
    SearchResults.at[index, 'GRAPH'] = Graph

   SearchResults = SearchResults.to_dict('records')
   return SearchResults

@callback(
    Output("CompanyOverview", "data", allow_duplicate=True),

    Output("BalanceSheet",'data', allow_duplicate=True),
    Output("IncomeStatement",'data', allow_duplicate=True),
    Output("CashflowStatement",'data', allow_duplicate=True),
    Output("FundamentalDataFrame","data",allow_duplicate=True),
    Output("MonthlyPriceInformation", "data", allow_duplicate=True),

    Output("location", "href"),

    Input("selection-single-grid", "cellClicked"),prevent_initial_call=True)

def GetSelectedStock(cell):
  if cell and cell['colId'] == "SYMBOL":
    Tag = cell['value']

    Receive_Dicts = APICalls.APIRequests

    DictCompanyOverview = Receive_Dicts.ReceiveCompanyOverview(Tag)
    DictBalanceSheetData = Receive_Dicts.ReturnFundamentalData(Tag, "BALANCE_SHEET")
    DictIncomestatementData = Receive_Dicts.ReturnFundamentalData(Tag, "INCOME_STATEMENT")
    DictCashFlowStatementData = Receive_Dicts.ReturnFundamentalData(Tag, "CASH_FLOW")
    DictMonthlyPriceInformationData = Receive_Dicts.ReceivePriceInformation("MONTHLY", Tag)
    DataObject = Dataprocessing.CreateDataFrames 

    MonthlyPriceDataFrame =  DataObject.CreatePriceDataFrame(DictMonthlyPriceInformationData,"Monthly Adjusted Time Series")

    dfBalanceAnnual,dfBalanceQuarterly,dfIncomeAnnual,dfIncomeQuarterly,dfCashFlowAnnual,dfCashFlowQuarterly = DataObject.CreateFundamentalDataFrames(DictBalanceSheetData,DictIncomestatementData,DictCashFlowStatementData)

    FundamentalDataFrame = DataObject.MergeFundamentalDataFrames(dfBalanceAnnual,dfBalanceQuarterly,dfIncomeAnnual,dfIncomeQuarterly,dfCashFlowAnnual,dfCashFlowQuarterly)

    FundamentalDataFrame = DataObject.MergeDataFrames(FundamentalDataFrame,MonthlyPriceDataFrame,['DatesForMerge'],"left")

    FundamentalDataFrame = DataObject.CleanDataFrame(FundamentalDataFrame,['index'])
    FundamentalDataFrame  = DataObject.ConvertToZero(FundamentalDataFrame,["netIncome","dividendPayoutPreferredStock"])

    FundamentalDataFrame = DataObject.ConvertToFloat(FundamentalDataFrame,["netIncome","dividendPayoutPreferredStock"])

    Averageslist = [["netIncomeAverage","netIncome"],["preferreddividendpayout","dividendPayoutPreferredStock"]]
    
    for List in Averageslist:
     FundamentalDataFrame = DataObject.CreateAverage(FundamentalDataFrame,List[0],List[1])

    FundamentalDataFrame= DataObject.AddEPSColumn(FundamentalDataFrame,DictCompanyOverview)

    FundamentalDataFrame= DataObject.AddColumn(FundamentalDataFrame,"Compensation", 1)
    FundamentalDataFrame["Compensation"] = FundamentalDataFrame["Compensation"].astype(float)
    
    RatioElements = [
    [["totalShareholderEquity"], ["totalAssets"], "Equity to Asset Ratio: "],
    [["totalLiabilities"], ["totalShareholderEquity"], "Debt to Equity Ratio: "],
    [["longTermDebt"], ["totalShareholderEquity"], "Long Term Debt to Equity Ratio: "],
    [["shortTermDebt"], ["totalShareholderEquity"], "Short Term Debt to Equity Ratio: "],
    [["totalNonCurrentAssets"], ["totalAssets"], "Fixed Asset Ratio: ",],
    [["totalShareholderEquity"], ["totalNonCurrentAssets"], "Coverage Ratio I: "],
    [["totalShareholderEquity","longTermDebt"], ["totalNonCurrentAssets"], "Coverage Ratio II: "],
    [["cashAndCashEquivalentsAtCarryingValue","cashAndShortTermInvestments"], ["totalCurrentLiabilities"],"Cash Ratio: "],
    [["cashAndCashEquivalentsAtCarryingValue","cashAndShortTermInvestments","currentNetReceivables"], ["totalCurrentLiabilities"],"Quick Ratio: "],
    [["totalCurrentAssets"], ["totalCurrentLiabilities"], "Current Ratio: "],
    [["netIncomeAverage"],["totalShareholderEquity"], "Return on Equity: "],
    [["netIncomeAverage"],["totalAssets"], "Return on Assets: "],
    [["ebit"],["totalRevenue"], "Return on Sales (EBIT-Margin): "],
    [["operatingIncome"],["totalRevenue"], "Operating Profit Margin: "],
    [["netIncome"],["totalRevenue"], "Profit Margin: "],
    [["ebit"],["interestExpense"], "Interest Coverage Ratio: "],
    [["operatingCashflow"],["totalRevenue"], "Operating Cashflow to Sales Ratio: "],
    [["EPS"], ["Compensation"], "Earnings per Share: "],
    [["Prices"], ["EPS"], "Price Earnings Ratio: "]]

    ColumnHeaders= [LastElement[-1] for LastElement in RatioElements]
    Numerators =[FirstElement[0] for FirstElement in RatioElements]
    Denumerators=[SecondElement[1] for SecondElement in RatioElements]




    for (Column, Numerator, Denumerator) in zip(ColumnHeaders, Numerators, Denumerators):
        FundamentalDataFrame[Column]= Ratios.CreateRatio(FundamentalDataFrame,Numerator,Denumerator)

    
    FundamentalDataFrame.to_excel("C:/Users/User/OneDrive/Desktop/FundamentalDataFrame.xlsx")
    FundamentalDataFrame =  FundamentalDataFrame.to_json(date_format='iso', orient='split')
    #MonthlyPriceDataFrame = MonthlyPriceDataFrame.to_json(date_format='iso', orient='split')

    return DictCompanyOverview, DictBalanceSheetData, DictIncomestatementData, DictCashFlowStatementData, FundamentalDataFrame, DictMonthlyPriceInformationData,"http://127.0.0.1:8050/stockbasics"   

  else:
    return dash.no_update

