import pandas as pd
from numerize import numerize

class CreateDataFrames:

    def CreateFundamentalDataFrames(BalanceSheet, IncomeStatement, CashflowStatement):

        dfBalanceAnnual = pd.DataFrame(BalanceSheet["annualReports"])
        dfBalanceQuarterly = pd.DataFrame(BalanceSheet["quarterlyReports"])
        dfIncomeAnnual = pd.DataFrame(IncomeStatement["annualReports"])
        dfIncomeQuarterly = pd.DataFrame(IncomeStatement["quarterlyReports"])
        dfCashFlowAnnual = pd.DataFrame(CashflowStatement["annualReports"])
        dfCashFlowQuarterly = pd.DataFrame(CashflowStatement["quarterlyReports"])
            
        return dfBalanceAnnual,dfBalanceQuarterly,dfIncomeAnnual,dfIncomeQuarterly,dfCashFlowAnnual,dfCashFlowQuarterly


    def MergeFundamentalDataFrames(dfBalanceAnnual,dfBalanceQuarterly,dfIncomeAnnual,dfIncomeQuarterly,dfCashFlowAnnual,dfCashFlowQuarterly):
        
        Quarterlies= pd.merge(pd.merge(dfBalanceQuarterly,dfIncomeQuarterly, on=['fiscalDateEnding','reportedCurrency'],  how="right"),dfCashFlowQuarterly,  on=['fiscalDateEnding','reportedCurrency',"netIncome"], how="right")
        Quarterlies['frequency'] = "quarterlyReports"

        Yearlies= pd.merge(pd.merge(dfBalanceAnnual,dfIncomeAnnual, on=['fiscalDateEnding','reportedCurrency'],  how="right"), dfCashFlowAnnual, on=['fiscalDateEnding','reportedCurrency',"netIncome"], how="right")
        Yearlies['frequency'] = "annualReports"

        df = pd.concat([Quarterlies,Yearlies], axis=0) 
        df = df.reset_index()
        df.to_excel('FundamentalDataFrameUnprocessed.xlsx')

        return df


    def ConvertToZero(Df, Columns):
        
       for Column in Columns:
        Df.loc[Df[Column] == "None",[Column]] = 0
        Df.loc[Df[Column] == None,[Column]] = 0


       return Df

    #def ConvertToZero(dfCashFlowAnnual, dfCashFlowQuarterly):
    
       # dfCashFlowAnnual.loc[dfCashFlowAnnual["netIncome"] == "None", ["netIncome"]] = 0
       # dfCashFlowAnnual.loc[dfCashFlowAnnual["dividendPayoutPreferredStock"] == "None", ["dividendPayoutPreferredStock"]] = 0

      #  dfCashFlowQuarterly.loc[dfCashFlowQuarterly["netIncome"] == "None", ["netIncome"]] = 0
       # dfCashFlowQuarterly.loc[dfCashFlowQuarterly["dividendPayoutPreferredStock"] == "None", ["dividendPayoutPreferredStock"]] = 0

      #  return dfCashFlowAnnual, dfCashFlowQuarterly

    def ConvertToFloat(Df, Columns):
       for Column in Columns:
        Df[Column] = Df[Column].astype(float)      
       return Df

   # def ConvertToFloat(dfIncomeAnnual,dfIncomeQuarterly,dfCashFlowAnnual,dfCashFlowQuarterly):

        #dfIncomeAnnual["netIncome"] = dfIncomeAnnual["netIncome"].astype(float)
        #dfIncomeQuarterly["netIncome"]  = dfIncomeQuarterly["netIncome"].astype(float)
   
       # dfCashFlowAnnual[["netIncome","dividendPayoutPreferredStock"]] =dfCashFlowAnnual[["netIncome","dividendPayoutPreferredStock"]].astype(float)
       # dfCashFlowQuarterly[["netIncome","dividendPayoutPreferredStock"]] =dfCashFlowQuarterly[["netIncome","dividendPayoutPreferredStock"]].astype(float)

      
       
     #  return dfIncomeAnnual,dfIncomeQuarterly,dfCashFlowAnnual,dfCashFlowQuarterly

    def CreateAverage(df, ResultColumn, OperatingColumn):
       
        df[ResultColumn] = df.loc[:,OperatingColumn] + df.loc[:,OperatingColumn].shift(-1)+df.loc[:,OperatingColumn].shift(-2)+df.loc[:,OperatingColumn].shift(-3)
        df.loc[df[df['frequency'] == "quarterlyReports"][-3:].index, ResultColumn] = None

        #df.loc[df["frequency"] == "quarterlyReports", [ResultColumn]]= None
        #dataframe.loc[(dataframe['Age'] == 21) &
              #dataframe['Stream'].isin(options)]
        #df.to_excel("XXXXXX.xlsx")

        df.loc[df["frequency"] == "annualReports", [ResultColumn]] = df[OperatingColumn]

       #df.loc[df["frequency"] == "quarterlyReports", [ResultColumn]].iloc[-3:]= None
       # df.to_excel("2323232X.xlsx")

        return df


       # RateFrame.loc[RateFrame['FullPercentage'] != "NaN", ['FullPercentage']] = RateFrame['FullPercentage']+" %"



    #def CreateAverage(dfIncomeAnnual,dfIncomeQuarterly,dfCashFlowAnnual,dfCashFlowQuarterly):

        #dfIncomeAnnual["netIncomeAverage"] = dfIncomeAnnual["netIncome"]
        #dfIncomeQuarterly["netIncomeAverage"]= dfIncomeQuarterly.loc[:,"netIncome"] + dfIncomeQuarterly.loc[:,"netIncome"].shift(-1)+dfIncomeQuarterly.loc[:,"netIncome"].shift(-2)+dfIncomeQuarterly.loc[:,"netIncome"].shift(-3)
       # dfIncomeQuarterly["netIncomeAverage"].iloc[-3:]= None

      #  dfCashFlowAnnual["netIncomeAverage"]=dfCashFlowAnnual["netIncome"]
      #  dfCashFlowQuarterly["netIncomeAverage"]= dfCashFlowQuarterly.loc[:,"netIncome"] + dfCashFlowQuarterly.loc[:,"netIncome"].shift(-1)+dfCashFlowQuarterly.loc[:,"netIncome"].shift(-2)+dfCashFlowQuarterly.loc[:,"netIncome"].shift(-3)
      #  dfCashFlowQuarterly["netIncomeAverage"].iloc[-3:]= None

      #  dfCashFlowAnnual["preferreddividendpayout"] = dfCashFlowAnnual["dividendPayoutPreferredStock"]
       # dfCashFlowQuarterly["preferreddividendpayout"]= dfCashFlowQuarterly.loc[:,"dividendPayoutPreferredStock"] + dfCashFlowQuarterly.loc[:,"dividendPayoutPreferredStock"].shift(-1)+dfCashFlowQuarterly.loc[:,"dividendPayoutPreferredStock"].shift(-2)+dfCashFlowQuarterly.loc[:,"dividendPayoutPreferredStock"].shift(-3)
      #  dfCashFlowQuarterly["preferreddividendpayout"].iloc[-3:]= None

    #    return dfIncomeAnnual,dfIncomeQuarterly,dfCashFlowAnnual,dfCashFlowQuarterly

    #def MergeFundamentalDataFrames(dfBalanceAnnual,dfBalanceQuarterly,dfIncomeAnnual,dfIncomeQuarterly,dfCashFlowAnnual,dfCashFlowQuarterly):
        
       # Quarterlies= pd.merge(pd.merge(dfBalanceQuarterly,dfIncomeQuarterly, on=['fiscalDateEnding','reportedCurrency'],  how="right"),dfCashFlowQuarterly,  on=['fiscalDateEnding','reportedCurrency',"netIncome","netIncomeAverage"], how="right")
       # Quarterlies['frequency'] = "quarterlyReports"

       # Yearlies= pd.merge(pd.merge(dfBalanceAnnual,dfIncomeAnnual, on=['fiscalDateEnding','reportedCurrency'],  how="right"), dfCashFlowAnnual, on=['fiscalDateEnding','reportedCurrency',"netIncome","netIncomeAverage"], how="right")
        #Yearlies['frequency'] = "annualReports"

       # df = pd.concat([Quarterlies,Yearlies], axis=0) 
      #  return df

    def AddEPSColumn(Fundamentaldataframe, CompanyOverview):
  
        SharesOutstanding = float(CompanyOverview["SharesOutstanding"])
        Fundamentaldataframe["EPS"]=((Fundamentaldataframe["netIncomeAverage"]-Fundamentaldataframe["preferreddividendpayout"])/SharesOutstanding).round(2)
        Fundamentaldataframe.to_excel('FundamentalDataFrame.xlsx')
        Fundamentaldataframe =  Fundamentaldataframe.to_json(date_format='iso', orient='split')
        return Fundamentaldataframe


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