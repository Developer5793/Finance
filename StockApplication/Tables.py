from dash import html
from dash import dash, dash_table
import pandas as pd
import datetime as dt


class Table:
    def __init__(self, df, ColumnName=None):
     self.df = df
     self.ColumnName = ColumnName


    def CreateRatioTable(self):

       ObjectTableFrame = self.df[["fiscalDateEnding","Divison","Percentage"]].copy()
       ObjectTableFrame["DivisionRateDelta"] = ObjectTableFrame["Divison"]- ObjectTableFrame["Divison"].shift(-1)
       ObjectTableFrame['Marker'] = ""

       ObjectTableFrame.loc[ObjectTableFrame["DivisionRateDelta"] > 0, ['Marker']] = '+'
       ObjectTableFrame.loc[ObjectTableFrame["DivisionRateDelta"] < 0, ['Marker']] = '-'
       ObjectTableFrame.loc[ObjectTableFrame["DivisionRateDelta"] == None, ['Marker']] = ''

       ObjectTableFrame['PercentageRateDelta'] = ObjectTableFrame.DivisionRateDelta*100
       ObjectTableFrame.loc[ObjectTableFrame["PercentageRateDelta"] == None, ['PercentageRateDelta']] = None

       ObjectTableFrame.PercentageRateDelta = ObjectTableFrame.PercentageRateDelta.astype(float)
       ObjectTableFrame.PercentageRateDelta = ObjectTableFrame.PercentageRateDelta.round(1)
       ObjectTableFrame.PercentageRateDelta =ObjectTableFrame.PercentageRateDelta.astype(str)
       ObjectTableFrame.loc[ObjectTableFrame['Marker'] == "+",["PercentageRateDelta"]] = ObjectTableFrame['Marker']+ObjectTableFrame['PercentageRateDelta']+" %"
       ObjectTableFrame.loc[ObjectTableFrame['Marker'] == "-",["PercentageRateDelta"]] = ObjectTableFrame['PercentageRateDelta']+" %"

       ObjectTableFrame.loc[ObjectTableFrame['PercentageRateDelta'] == "nan",["PercentageRateDelta"]] = "N/A"

       ObjectTableCleaned = ObjectTableFrame[["fiscalDateEnding",'Percentage','PercentageRateDelta']].copy()
       ObjectTableCleaned['fiscalDateEnding'] = pd.to_datetime(ObjectTableCleaned['fiscalDateEnding'], errors='coerce')

       ObjectTableCleaned['fiscalDateEnding'] =  ObjectTableCleaned['fiscalDateEnding'].dt.strftime('%Y-%m-%d')

       ObjectTableCleaned = ObjectTableCleaned.rename(columns={'fiscalDateEnding': 'Fiscal Date Ending:','Percentage': self.ColumnName,'PercentageRateDelta':'Delta:'})


       RatioTable = dash_table.DataTable(ObjectTableCleaned.to_dict('records'),columns=[{"name": i, "id": i} for i in ObjectTableCleaned.columns],
       style_cell={'fontSize':12, 'font-family':'sans-serif','font-family':'sans-serif' },                                       
       style_cell_conditional=[
        {'if': {'column_id': 'Fiscal Date Ending:'},
         'width': '80px'},
        {'if': {'column_id': self.ColumnName},
         'width': '100px'},
        {'if': {'column_id': 'Delta'},
         'width': '60px'}],
        style_header={
        'backgroundColor': 'white',
        'color': 'black',
        'fontWeight': 'bold'
        }, 
        style_data={
        'color': 'black',
        'backgroundColor': 'white'
        },
        )
       RatioTable = html.Div(RatioTable, style={'marginLeft': '15px',
                                                'marginRight': '15px',
                                                'width': "320px",
                                                'marginTop': "20px"})
       return RatioTable

    def CreateSearchTableDataFrame(self):
       
     Object = pd.read_json(self.df, orient='split')

     SearchTableDataFrame = Object[["1. symbol","2. name","4. region", "8. currency"]].copy()
     SearchTableDataFrame.rename(columns={'1. symbol': "SYMBOL", '2. name': 'NAME',"4. region":"REGION","8. currency": "CURRENCY"}, inplace=True)
     SearchTableDataFrame["GRAPH"]=""
     return SearchTableDataFrame



    def CreateOverviewTableDataFrame (self, TableColumns):

        dfCompanyOverview = self.df[TableColumns]
        dfCompanyOverviewT = dfCompanyOverview.transpose()
        dfCompanyOverviewT = dfCompanyOverviewT.reset_index()
        dfCompanyOverviewT.rename({'index': 'NAME', 0: 'VALUE'}, axis=1, inplace=True)
        dfCompanyOverviewT = dfCompanyOverviewT.to_dict('records')
        return dfCompanyOverviewT

       
   



