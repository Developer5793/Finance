from dash import dcc
import pandas as pd
import plotly.graph_objects as go
import requests
import plotly.express as px


class DrawGraphs:

    def DrawRatioGraphs(RateFrame, AxisName):

        layout = dict(
                 plot_bgcolor='#191919', 
                 paper_bgcolor='#191919',
                 height = 320, width=320,
                 margin=dict(l=10, r=10, t=50, b=20),

                  xaxis=dict(title='Year',
                        title_font=dict(size=14, family='Courier', color='white'),
                         #linecolor='white',
                         color ='white',
                         showgrid=False,
                         mirror=True),

                  yaxis=dict(title=AxisName,
                         linecolor='white',
                         titlefont=dict(size=14, family='Courier', color='white'),
                         color ='white',
                         tickformat = '.1%',
                         showgrid=False,
                         mirror=False)
        )   

        if "annualReports" in RateFrame.frequency.values: 
         data= go.Scatter(x=RateFrame['fiscalDateEnding'],
                         y=RateFrame['Divison'],                                                
                         mode="markers+text",
                         marker = {'color' : '#FFBA0D'},
                         text= RateFrame['FullPercentage'],
                         textposition='top center',
                         cliponaxis=False,
                         textfont=dict(color='#FFBA0D',size=10))
         Figure = go.Figure(data=data, layout=layout)
         Figure.update_yaxes(rangemode='tozero')
         Figure.update_xaxes(automargin=True)
         Figure=dcc.Graph(figure=Figure)
         return Figure

        if "quarterlyReports" in RateFrame.frequency.values: 
         data= go.Scatter(x=RateFrame['fiscalDateEnding'],
                         y=RateFrame['Divison'],                                                
                         mode="markers+text",
                         marker = {'color' : '#FFBA0D'},
                         text= " ",
                         textposition='top center',
                         cliponaxis=False,
                         textfont=dict(color='#FFBA0D',size=10))
         Figure = go.Figure(data=data, layout=layout)
         Figure.update_yaxes(rangemode='tozero')
         Figure.update_xaxes(automargin=True)
         Figure=dcc.Graph(figure=Figure)
         return Figure


     
    def DrawTableChart(PriceDataFrame):       
     Figure = px.line(
        PriceDataFrame,
        x="Dates",
        y="Prices",
     )
     Figure.update_layout(
        showlegend=False,
        yaxis=dict(visible=False,showticklabels=False),
        xaxis=dict(visible=False, showticklabels=False),

        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        hovermode="closest",
        height=60
     )

     if PriceDataFrame.loc[0, 'Prices'] < PriceDataFrame.loc[52, 'Prices']:
       Figure.update_traces(line_color='red', hovertemplate = 'Price: %{y:$.2f}<br>Date: %{x}')

     if PriceDataFrame.loc[0, 'Prices'] > PriceDataFrame.loc[52, 'Prices']:
       Figure.update_traces(line_color='green', hovertemplate = 'Price: %{y:$.2f}<br>Date: %{x}')

     return Figure

    
    def DrawChart(PriceDataFrame):
     Figure = px.line(
        PriceDataFrame,
        x="Dates",
        y="Prices",
     )
     Figure.update_layout(
        showlegend=False,
        xaxis=dict(showgrid=False, visible=True, showticklabels=True, title=None),
        #yaxis_title=None,
        yaxis=dict(showgrid=False, showticklabels=True, visible=True, title=None),
        margin=dict(l=0, r=0, t=50, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        #hovermode="closest",
        height=400
     )

     #if PriceDataFrame.loc[0, 'Prices'] < PriceDataFrame.loc[52, 'Prices']:
     Figure.update_traces(hovertemplate = 'Price: %{y:$.2f}<br>Date: %{x}', line_color="green")
     Figure.update_yaxes(title_font_color="white", linecolor='white', ticks="outside", tickcolor="white", tickfont_color="white", zeroline=False, tickprefix="$", tickformat=".2f")
     Figure.update_xaxes(title_font_color="white", linecolor='white',ticks="outside", tickcolor="white", tickfont_color="white", zeroline=False)


     Figure = dcc.Graph(figure=Figure)

     return Figure
     #if PriceDataFrame.loc[0, 'Prices'] > PriceDataFrame.loc[52, 'Prices']:
      # Figure.update_traces(line_color='green', hovertemplate = 'Price: %{y:$.2f}<br>Date: %{x}')

