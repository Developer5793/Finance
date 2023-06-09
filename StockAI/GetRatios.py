import pandas as pd
import numpy as np
pd.options.mode.chained_assignment = None  



class Ratios:

   def CreateRatioMuster(FundamentalDataFrame, NumeratorList, DenominatorList):

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


   def CreateRatio(FundamentalDataFrame, NumeratorList, DenominatorList):
       
       temp = pd.DataFrame()

   
       FundamentalDataFrame[NumeratorList] = FundamentalDataFrame[NumeratorList].astype(float)
 
       temp['Numerator']=FundamentalDataFrame.loc[:,NumeratorList].sum(axis=1, min_count=1)
       
       FundamentalDataFrame[DenominatorList] = FundamentalDataFrame[DenominatorList].astype(float)
       temp['Denominator']=FundamentalDataFrame.loc[:,DenominatorList].sum(axis=1, min_count=1)

       temp.loc[(temp['Numerator'] == np.NaN),'Divison'] =  np.nan
       temp.loc[(temp['Denominator'] != 0) & (temp['Denominator']!= np.nan),'Divison'] =  temp['Numerator']/temp['Denominator']
       temp.loc[(temp['Denominator'] == np.nan),'Divison'] =  np.nan
       temp.loc[(temp['Denominator'] == 0),'Divison'] =  np.nan

       return temp.Divison


   def CreateGraphRatio(FundamentalDataFrame, Column, Operation, Symbol):

       FundamentalDataFrame = pd.read_json(FundamentalDataFrame, orient='split')
       temp = pd.DataFrame()

       temp['fiscalDateEnding'] = FundamentalDataFrame['fiscalDateEnding']
       temp["frequency"] = FundamentalDataFrame["frequency"]
       temp["Divison"] = FundamentalDataFrame[Column]

       if Operation == "Multiple":
         temp['Result'] =  temp["Divison"]
       else:
         temp['Result'] =  temp["Divison"]*100 


       temp['RoundedResult'] = temp['Result']

       temp.Result = temp.Result.astype(float)
       temp.Result = temp.Result.round(1)
       temp.Result = temp.Result.astype(str)
       temp.loc[temp['Result'] != "nan",["Result"]] = temp['Result']+Symbol#" %" #Symbol
       temp.loc[temp['Result'] == "nan",["Result"]] = "N/A or 0"
       

       temp['RoundedResult'] = temp['RoundedResult'].fillna(-1)
       temp.loc[~np.isfinite(temp['RoundedResult']), 'RoundedResult'] = -1  
       temp['RoundedResult'] = temp['RoundedResult'].astype(int)
       temp['RoundedResult'] = temp['RoundedResult'].astype(str)
       temp['RoundedResult'] = temp['RoundedResult'].replace('-1', str(np.nan))
       temp.loc[temp['RoundedResult'] != str(np.nan), ['RoundedResult']] = temp['RoundedResult']+Symbol#" %"


       AnnualRatios = temp[temp['frequency'] == 'annualReports']
       QuarterlyRatios = temp[temp['frequency'] == 'quarterlyReports']
       CurrentQuarterlyRatio = temp.iloc[0]['Result'] 

       return  CurrentQuarterlyRatio, AnnualRatios,  QuarterlyRatios 



