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
import DisplayElementsClass
import Dataprocessing
import APICalls



class RatioElement (DisplayElementsClass.RatioDisplayElements):
 def __init__(self, StateButton, Numerators, Denominators, SidebarName, RatioDisplayElements):

     self.StateButton = StateButton
     self.YearlyButton = RatioDisplayElements.YearlyButton
     self.QuarterlyButton = RatioDisplayElements.QuarterlyButton
     self.TableButton = RatioDisplayElements.TableButton
     self.RatioPercentage = RatioDisplayElements.RatioPercentage
     self.GraphORTableObject = RatioDisplayElements.GraphORTableObject
     self.Numerators = Numerators
     self.Denominators = Denominators
     self.SidebarName = SidebarName
        


 def RatioCallback(self):

     @callback(
            Output(self.StateButton, 'data', allow_duplicate=True),
            Input(self.YearlyButton ,'n_clicks'),
            prevent_initial_call=True)

     def update_LastButtonpressed(n_clicks):
            if n_clicks is None:
                raise PreventUpdate
            return "YearlyButtonPressed"

     @callback(
            Output(self.StateButton , 'data',allow_duplicate=True),
            Input(self.QuarterlyButton,'n_clicks'),
            prevent_initial_call=True
        )
     def update_LastButtonpressed(n_clicks):
            if n_clicks is None:
                raise PreventUpdate
            return "QuarterlyButtonPressed" 

     @callback(
            Output(self.StateButton, 'data'),
            Input(self.TableButton,'n_clicks'),
            prevent_initial_call=True
            )
     def update_LastButtonpressed(n_clicks):
            if n_clicks is None:
                raise PreventUpdate
            return "TableButtonPressed"

     @callback(
            #Initalize this years Balance Sheet Ratio
            Output(self.RatioPercentage, 'children'),
            Output(self.GraphORTableObject,'children'),
            Input("FundamentalDataFrame", 'modified_timestamp'),
            Input( self.StateButton,'modified_timestamp'),
            State("FundamentalDataFrame",'data'), 
            State(self.StateButton,"data"))
 
     def Update_EquityToAssets(ts, ts2, FundamentalDataFrame, ButtonState):
           if ts is None or ts2 is None or FundamentalDataFrame is None:
               print("CALLBACK FAILED")
              # print (FundamentalDataFrame)
               raise PreventUpdate
           Numerators= self.Numerators
           Denominators=self.Denominators 
           print("Callback executed")

           FundamentalData = GetRatios.Ratios
           RatioCurrentQuarter, AnnualRatios, QuarterlyRatios = FundamentalData.CreateRatio(FundamentalDataFrame, Numerators, Denominators)
           FundamentalGraphs=Graphs.DrawGraphs

           if ButtonState == None and FundamentalDataFrame:
            AnnualGraph = FundamentalGraphs.DrawRatioGraphs(AnnualRatios, self.SidebarName )
            return RatioCurrentQuarter, AnnualGraph

           if ButtonState == "YearlyButtonPressed" and ButtonState != "QuarterlyButtonPressed" and FundamentalDataFrame:
            AnnualGraph = FundamentalGraphs.DrawRatioGraphs(AnnualRatios,  self.SidebarName )
            return RatioCurrentQuarter, AnnualGraph
    
           if ButtonState == "QuarterlyButtonPressed" and FundamentalDataFrame and ButtonState != "YearlyButtonPressed":
            QuarterlyGraph = FundamentalGraphs.DrawRatioGraphs(QuarterlyRatios,  self.SidebarName )
            return RatioCurrentQuarter, QuarterlyGraph

           if ButtonState == "TableButtonPressed" and FundamentalDataFrame:
            RatioTable = Tables.Table(AnnualRatios, self.SidebarName)
            Table = RatioTable.CreateRatioTable()
            return RatioCurrentQuarter, Table

           else:
            raise PreventUpdate

