import pandas as pd
from numerize import numerize

class CreateDataFrames:

    def CreateFundamentalDataFrame(BalanceSheet, IncomeStatement, CashflowStatement):

        dfBalanceAnnual = pd.DataFrame(BalanceSheet["annualReports"])

        dfBalanceQuarterly = pd.DataFrame(BalanceSheet["quarterlyReports"])

        dfIncomeAnnual = pd.DataFrame(IncomeStatement["annualReports"])

        dfIncomeQuarterly = pd.DataFrame(IncomeStatement["quarterlyReports"])
       
        dfCashFlowAnnual = pd.DataFrame(CashflowStatement["annualReports"])

        dfCashFlowQuarterly = pd.DataFrame(CashflowStatement["quarterlyReports"])

        Quarterlies= pd.merge(pd.merge(dfBalanceQuarterly,dfIncomeQuarterly, on=['fiscalDateEnding','reportedCurrency'],  how="right"),dfCashFlowQuarterly,  on=['fiscalDateEnding','reportedCurrency',"netIncome"], how="right")
        Quarterlies['frequency'] = "quarterlyReports"

        Yearlies= pd.merge(pd.merge(dfBalanceAnnual,dfIncomeAnnual, on=['fiscalDateEnding','reportedCurrency'],  how="right"), dfCashFlowAnnual, on=['fiscalDateEnding','reportedCurrency',"netIncome"], how="right")
        Yearlies['frequency'] = "annualReports"

        result = pd.concat([Quarterlies,Yearlies], axis=0)  
        
        df =  result.to_json(date_format='iso', orient='split')
        return df

    def CreateSearchResultDataFrame(SearchResults):

        df = pd.DataFrame(SearchResults["bestMatches"]) 
        df = df.loc[df["4. region"] == "United States"]
        df = df.loc[df["3. type"] == "Equity"]
        df =  df.to_json(date_format='iso', orient='split')
        return df

    def CreateCompanyOverviewData(OverviewData):

       CompanyName = OverviewData.get('Name')
       CompanySymbol = OverviewData.get('Symbol')
       CompanyDescription = OverviewData.get('Description')
   
       dfCompanyOverview = pd.DataFrame([OverviewData])
       #dfCompanyOverviewx = dfCompanyOverview.drop(columns=["Exchange","Currency","Country","Sector","Industry","Address",'Name','Symbol','Description',"CIK"]) 

       return CompanyName, CompanySymbol, CompanyDescription, dfCompanyOverview
        
   
    def CreateWeeklyChart(PriceData): 
        DateList=[]
        PriceList=[]
  
        for x in PriceData["Weekly Adjusted Time Series"]:
            DateList.append(x)
            PriceList.append(PriceData["Weekly Adjusted Time Series"][x]["5. adjusted close"])

        PriceDataFrame =  pd.DataFrame(
            {'Dates': DateList,
             'Prices': PriceList,
            })
        PriceDataFrame["Prices"]=pd.to_numeric(PriceDataFrame["Prices"])
        #PriceDataFrame['Dates'] = pd.to_datetime(PriceDataFrame['Dates'], errors='coerce')

        return PriceDataFrame


    def MakeDataFrameHumandReadable(Companyoverview, Columnames):

        for Column in Columnames:
           Companyoverview[Column]= Companyoverview[Column].astype(float)
           Companyoverview[Column]= Companyoverview[Column].apply(lambda x: numerize.numerize(x))

        return Companyoverview