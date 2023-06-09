import requests
import random
from sqlalchemy import create_engine
import pandas as pd

class APIRequests:  

   def ReturnFundamentalData(tag, ReceiveType):
    

    url = 'https://www.alphavantage.co/query?function='+ReceiveType+'&symbol='+tag+'&apikey=8FE7NW93X6D8T1AX'
    r = requests.get(url)
    Data = r.json()
    return Data
  

   def SearchEndpoint(search_value):
    url = 'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords='+search_value+'&apikey=8FE7NW93X6D8T1AX'
    r = requests.get(url)
    Data = r.json()
    return Data 

   def ReceiveCompanyOverview(tag):
    url = 'https://www.alphavantage.co/query?function=OVERVIEW&symbol='+tag+'&apikey=8FE7NW93X6D8T1AX'
    r = requests.get(url)
    Data = r.json()
    return Data

   def ReceivePriceInformation(frequency, tag):
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_'+frequency+'_ADJUSTED&symbol='+tag+'&apikey=8FE7NW93X6D8T1AX'
    r = requests.get(url)
    Data = r.json()
    return Data


class SQLQueries:
   def __init__(self, Tablename):
    self.DRIVER="ODBC Driver 17 for SQL Server"
    self.server="DESKTOP-23QVBVH\SQLEXPRESS"
    self.DATABASE="Stocks"
    self.str_conn = f'mssql+pyodbc://{self.server}/{self.DATABASE}?driver={self.DRIVER}'
    self.engine = create_engine(self.str_conn, use_setinputsizes=False)
    self.connection = self.engine.connect()
    self.Tablename = Tablename

   def CreateSQLTable(self):
    Prices=pd.read_sql(self.Tablename , self.connection)
    Prices['Prices'] = Prices['Prices'].astype('float')
    return Prices

