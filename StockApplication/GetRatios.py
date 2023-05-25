import pandas as pd
import numpy as np
pd.options.mode.chained_assignment = None  



class Ratios:

   def CreateRatio(FundamentalDataFrame, NumeratorList, DenominatorList):

       FundamentalDataFrame = pd.read_json(FundamentalDataFrame, orient='split')
       RateFrame = FundamentalDataFrame[NumeratorList+DenominatorList+["fiscalDateEnding","frequency"]].copy()      

       RateFrame['Numerator']=RateFrame.loc[:,NumeratorList].sum(axis=1)
      
       RateFrame['Denominator']=RateFrame.loc[:,DenominatorList].sum(axis=1)

       RateFrame['Divison'] =  RateFrame['Numerator']/RateFrame['Denominator']

       RateFrame['Percentage'] = RateFrame.Divison*100
       RateFrame['FullPercentage'] = RateFrame['Percentage']

       RateFrame['FullPercentage'] = np.round(pd.to_numeric(RateFrame['FullPercentage'], errors='coerce')).astype('Int64')
       RateFrame['FullPercentage'] = RateFrame['FullPercentage'].astype(str)
       RateFrame.loc[RateFrame['FullPercentage'] != "NaN", ['FullPercentage']] = RateFrame['FullPercentage']+" %"

       RateFrame.Percentage = RateFrame.Percentage.astype(float)
       RateFrame.Percentage = RateFrame.Percentage.round(1)
       RateFrame.Percentage =RateFrame.Percentage.astype(str)
       RateFrame.loc[RateFrame['Percentage'] != "NaN",["Percentage"]] = RateFrame['Percentage']+" %"

       AnnualRatios = RateFrame[RateFrame['frequency'] == 'annualReports']
       QuarterlyRatios = RateFrame[RateFrame['frequency'] == 'quarterlyReports']

       CurrentQuarterlyRatio = QuarterlyRatios.iloc[0]['Percentage']


  
       return CurrentQuarterlyRatio, AnnualRatios,  QuarterlyRatios 


   