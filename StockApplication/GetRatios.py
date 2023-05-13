import pandas as pd
import numpy as np
pd.options.mode.chained_assignment = None  



class Ratios:

   def CreateRatio(FundamentalDataFrame, NumeratorList, DenominatorList):

       FundamentalDataFrame = pd.read_json(FundamentalDataFrame, orient='split')
       RateFrame = FundamentalDataFrame[NumeratorList+DenominatorList+["fiscalDateEnding","frequency"]].copy()


       ###This Lines add the Incomestatements of the last 4 Quarters up to build a ratio for every quarter####
       if (NumeratorList == ["netIncome"] and DenominatorList == ["totalShareholderEquity"]) or (DenominatorList == ["totalAssets"] and NumeratorList == ["netIncome"]):      
        RateFrameQuarter = RateFrame[RateFrame['frequency'] == 'quarterlyReports']
        RateFrameQuarter["Numerator"] = (RateFrameQuarter.loc[:,NumeratorList] + RateFrameQuarter.loc[:,NumeratorList].shift(-1)+RateFrameQuarter.loc[:,NumeratorList].shift(-2)+RateFrameQuarter.loc[:,NumeratorList].shift(-3)).sum(axis=1)
        RateFrameQuarter.iloc[-3:]=None
        RateFrameAnnual = RateFrame[RateFrame['frequency'] == 'annualReports']
        RateFrameAnnual['Numerator']=RateFrameAnnual.loc[:,NumeratorList].sum(axis=1)
        RateFrame = pd.concat([RateFrameQuarter,RateFrameAnnual])

       else:
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


