# import webdriver
import time
import pandas as pd
import numpy as np

from selenium import webdriver
from selenium.webdriver.common.by import By
# import Action chains 
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

# improt exeptions if element is not found
from selenium.common.exceptions import NoSuchElementException
is_tag = input("Enter a tag please: ")
# create webdriver object
driver = webdriver.Edge()


#is_link='https://finance.yahoo.com/quote/BRYN/key-statistics?p=BRYN'

#is_link='https://finance.yahoo.com/quote/BAC/key-statistics?p=BAC'

#is_link ='https://finance.yahoo.com/quote/PYPL/key-statistics?p=PYPL'

is_link ='https://finance.yahoo.com/quote/' + is_tag + '/key-statistics?p=' + is_tag



IncomeStatementSummary = pd.DataFrame()
BalanceSheetSummary = pd.DataFrame()


# get yahoo finance.com
driver.get(is_link)
time.sleep(5)
################ German 2 Accept Windows ###############
# get element 
element = driver.find_element(By.XPATH, '//button[@class="btn primary"]')
# create action chain object
action = ActionChains(driver)
# click the item
action.click(on_element = element)
# perform the operation
action.perform()

time.sleep(5)


# Same for second pop up Window
element2= driver.find_element(By.XPATH, '//button[@class="Mx(a) Fz(16px) Fw(600) Mt(20px) D(n)--mobp"]')

action = ActionChains(driver)
action.click(on_element = element2)
action.perform()
time.sleep(8)







####Algorithm to replace Billion/Million/k with numbers and 0.0000 with N/A #####
def Billion_Million_kor_NA(param):
    if param.endswith('B') or param.endswith('M') or param.endswith('k'):
      count = 0
      trigger= 0
      for dot in param:
        if trigger>0:
            count = count+1
        if dot == ".":
            trigger = 1 

      paramProcessed = param.replace(".","")
    
      if count == 3 and paramProcessed.endswith('B'):
        paramProcessed = paramProcessed[:-1]
        paramProcessed = paramProcessed + "0000000"
    
      if count == 2 and paramProcessed.endswith('B'):
        paramProcessed = paramProcessed[:-1]
        paramProcessed = paramProcessed + "00000000"

      if (count == 1 and paramProcessed.endswith('B')) or (count==0 and paramProcessed.endswith('B')):
        paramProcessed = paramProcessed[:-1]
        paramProcessed = paramProcessed + "000000000"
    
      if count == 3 and paramProcessed.endswith('M'):
        paramProcessed = paramProcessed[:-1]
        paramProcessed = paramProcessed + "0000"
    
      if count == 2 and paramProcessed.endswith('M'):
        paramProcessed = paramProcessed[:-1]
        paramProcessed = paramProcessed + "00000"

      if (count == 1 and paramProcessed.endswith('M')) or (count==0 and paramProcessed.endswith('M')):
        paramProcessed = paramProcessed[:-1]
        paramProcessed = paramProcessed + "000000"
 
      if count == 3 and paramProcessed.endswith('k'):
        paramProcessed = paramProcessed[:-1]
        paramProcessed = paramProcessed + "0"
    
      if count == 2 and paramProcessed.endswith('k'):
        paramProcessed = paramProcessed[:-1]
        paramProcessed = paramProcessed + "00"

      if (count == 1 and paramProcessed.endswith('k')) or (count==0 and paramProcessed.endswith('k')):
        paramProcessed = paramProcessed[:-1]
        paramProcessed = paramProcessed + "000"

      paramProcessed=int(paramProcessed)
    
    elif param == "N/A" or param.startswith("0.0000") or param.startswith("-0.0000") or param.startswith("+0.0000"):
        param ="N/A"
        paramProcessed = param

    else:
        paramProcessed = float(param)
    

    return paramProcessed


try:
    ####Collect full Statistics##############################
    dataStatistics = driver.find_elements(By.XPATH, '//td[contains(@class, "Pos(st) Start(0) Bgc($lv2BgColor) fi-row:h_Bgc($hoverBgColor) Pend(10px)  Miw(140px)") or contains(@class, "Fw(500) Ta(end) Pstart(10px) Miw(60px)") or contains(@class, "Pos(st) Start(0) Bgc($lv2BgColor) fi-row:h_Bgc($hoverBgColor) Pend(10px) ")]')
    DataStatisticsList = []

    #Collect all Names and Values from Statistics Site
    for value in dataStatistics:
     DataStatisticsList.append(value.text)

    #Create Columns Names and Append tag to it
    ColumnNames = DataStatisticsList[::2]
    ColumnNames.insert(0, "tag")
 
    #Create a List that contains all all Statistics Values
    Data = DataStatisticsList[1::2]
    Data.insert(0,is_tag)

    print(len(ColumnNames))
    print(len(Data))

    ##Crate Empty Dataframe with 61 Columns
    Stats = pd.DataFrame(pd.np.empty((0, 61)))
    #Add Columns and Data
    Stats.columns = ColumnNames
    Stats.loc[len(Stats)] = Data
    print(Stats.to_string())   

except NoSuchElementException:
       print("Element not found: ", is_tag)



######################################################

#Go to next page "Financials"
element3 = driver.find_element(By.XPATH, '//ul[@class="List(n) Whs(nw) fin-tab-items W(100%) Lh(1.7) H(44px) Bdbs(s) BdB(4px) Cf Mb(15px) Bdbc($seperatorColor) "]/li[7]/a[1]')
action = ActionChains(driver)
action.click(on_element = element3)
action.perform()
time.sleep(5)

#Get Income Common Stockholders 
element4 = driver.find_element(By.XPATH, '//button[@aria-label="Net Income Common Stockholders"]')
action = ActionChains(driver)
action.click(on_element = element4)
action.perform()
time.sleep(5)


####Here we collect the income statement in full########
dataIS = driver.find_elements(By.XPATH, '//div[contains(@class, "Ta(c) Py(6px) Bxz(bb) BdB Bdc($seperatorColor) Miw(120px) Miw(100px)--pnclg Bgc($lv1BgColor) fi-row:h_Bgc($hoverBgColor) D(tbc)") or contains(@class, "Ta(c) Py(6px) Bxz(bb) BdB Bdc($seperatorColor) Miw(120px) Miw(100px)--pnclg D(tbc)")]')
column_headersIS = driver.find_elements(By.XPATH, '//div[contains(@class, "D(ib) Va(m) Ell Mt(-3px) W(215px)--mv2 W(200px) undefined") or contains(@class, "D(ib) Va(m) Ell Mt(-3px) W(200px)--mv2 W(185px) undefined")]')
Dates = driver.find_elements(By.XPATH,  '//div[contains(@class, "Ta(c) Py(6px) Bxz(bb) BdB Bdc($seperatorColor) Miw(120px) Miw(100px)--pnclg D(ib) Fw(b) Tt(u) Bgc($lv1BgColor)") or contains(@class, "Ta(c) Py(6px) Bxz(bb) BdB Bdc($seperatorColor) Miw(120px) Miw(100px)--pnclg D(ib) Fw(b)")]')

IncomeStatementHeaders = []
IncomeStatementData =[]
DatesColumn=[]

for value in column_headersIS:
     IncomeStatementHeaders.append(value.text)

for value in dataIS:
     IncomeStatementData.append(value.text)
     
for value in Dates:
     DatesColumn.append(value.text)
     

#print('Data --> {}'.format(len(dataIS)))
print('ColumnHeaders --> {}'.format(len(column_headersIS)))

######Chunck size is len of Dates column
chunk_size = len(DatesColumn)
ListOfListsIS = list()

for i in range(0, len(IncomeStatementData), chunk_size):
    ListOfListsIS.append(IncomeStatementData[i:i+chunk_size])


FirstIncomeStatementYearly = pd.DataFrame()
 
#Add Rows with Chunk size
for z in range(0, len(IncomeStatementHeaders), 1):
    FirstIncomeStatementYearly[z] = ListOfListsIS[z]

FirstIncomeStatementYearly.columns = IncomeStatementHeaders


FirstIncomeStatementYearly.insert(0, "tag", is_tag)
FirstIncomeStatementYearly.insert(1, "Dates", DatesColumn)

IncomeStatementSummary = FirstIncomeStatementYearly

#####Done with income Statement########


#Go to Balance Sheet
BalanceSheetBtn = driver.find_element(By.XPATH, '//div[@class="Fw(500) D(ib) Pend(10px) H(18px) BdEnd Bdc($seperatorColor)"]')
action = ActionChains(driver)
action.click(on_element = BalanceSheetBtn)
action.perform()
time.sleep(5)


####Open subaccounts of BalanceSheet
try:
    TotalAssetsBtn = driver.find_element(By.XPATH,  '//button[@aria-label="Total Assets"]')
    action = ActionChains(driver)
    action.click(on_element = TotalAssetsBtn)
    action.perform()
    time.sleep(0.2)

    TotalLiabilitiesBtn = driver.find_element(By.XPATH,  '//button[@aria-label="Total Liabilities Net Minority Interest"]')
    action = ActionChains(driver)
    action.click(on_element = TotalLiabilitiesBtn)
    action.perform()
    time.sleep(0.2)

    TotalEquityBtn = driver.find_element(By.XPATH,  '//button[@aria-label="Total Equity Gross Minority Interest"]')
    action = ActionChains(driver)
    action.click(on_element = TotalEquityBtn)
    action.perform()
    time.sleep(0.2)

except NoSuchElementException:
    print("Element not found")


####Here we collect the Balance Sheet in full########
try:
    dataBS = driver.find_elements(By.XPATH, '//div[contains(@class, "Ta(c) Py(6px) Bxz(bb) BdB Bdc($seperatorColor) Miw(120px) Miw(100px)--pnclg D(tbc)") or contains(@class, "Ta(c) Py(6px) Bxz(bb) BdB Bdc($seperatorColor) Miw(120px) Miw(100px)--pnclg Bgc($lv1BgColor) fi-row:h_Bgc($hoverBgColor) D(tbc)")]')
    DatesBS = driver.find_elements(By.XPATH,'//div[contains(@class, "Ta(c) Py(6px) Bxz(bb) BdB Bdc($seperatorColor) Miw(120px) Miw(100px)--pnclg D(ib) Fw(b)") or contains(@class, "Ta(c) Py(6px) Bxz(bb) BdB Bdc($seperatorColor) Miw(120px) Miw(100px)--pnclg D(ib) Fw(b) Bgc($lv1BgColor)")]' )
    column_headersBS = driver.find_elements(By.XPATH,'//div[contains(@class, "D(ib) Va(m) Ell Mt(-3px) W(215px)--mv2 W(200px) undefined") or contains(@class, "D(ib) Va(m) Ell Mt(-3px) W(200px)--mv2 W(185px) undefined")]' )


    #print('Data --> {}'.format(len(dataBS)))
    print('ColumnHeaders --> {}'.format(len(column_headersBS)))

    BalanceSheetData = []
    BSColumnHeadersList =[]
    DatesBSList = []
    
    for value in  column_headersBS:
     BSColumnHeadersList.append(value.text)

    for value in dataBS:
     BalanceSheetData.append(value.text)

    for value in DatesBS:
     DatesBSList.append(value.text) 

    
    ListOfListsBS = list()
    chunk_size_BS = len(DatesBSList)

    for i in range(0, len(BalanceSheetData), chunk_size_BS):
        ListOfListsBS.append(BalanceSheetData[i:i+chunk_size_BS])

    BalanceSheetYearly= pd.DataFrame()

    for z in range(0, len(BSColumnHeadersList), 1):
     BalanceSheetYearly[z] = ListOfListsBS[z]
    
    BalanceSheetYearly.columns = BSColumnHeadersList

    BalanceSheetYearly.insert(0, "tag", is_tag)
    BalanceSheetYearly.insert(1, "Dates", DatesBSList)

except NoSuchElementException:
 print("Balance Sheet not found")
    

time.sleep(1)
   

 #### End of Balance Sheet Collection ########


taglist =["AAPL", "MSFT", "PYPL", "TSLA"]


def Statistics(tag):
       
        inputElement = driver.find_element(By.ID, "yfin-usr-qry")
        inputElement.send_keys(tag)
        inputElement.send_keys(Keys.ENTER)
        time.sleep(5)

        StatisticsBtn = driver.find_element(By.XPATH,  '//ul[@class="List(n) Whs(nw) fin-tab-items W(100%) Lh(1.7) H(44px) Bdbs(s) BdB(4px) Cf Mb(15px) Bdbc($seperatorColor) "]/li[4]/a[1]')
        action = ActionChains(driver)
        action.click(on_element = StatisticsBtn)
        action.perform()
        time.sleep(5)


        dataStatistics = driver.find_elements(By.XPATH, '//td[contains(@class, "Pos(st) Start(0) Bgc($lv2BgColor) fi-row:h_Bgc($hoverBgColor) Pend(10px)  Miw(140px)") or contains(@class, "Fw(500) Ta(end) Pstart(10px) Miw(60px)") or contains(@class, "Pos(st) Start(0) Bgc($lv2BgColor) fi-row:h_Bgc($hoverBgColor) Pend(10px) ")]')
        DataStatisticsListAlgo=[]


        #Collect all Names and Values from Statistics Site
        for value in dataStatistics:
         DataStatisticsListAlgo.append(value.text)

        print(len(DataStatisticsListAlgo))

 
        #Create a List that contains all all Statistics Values
        DataAlgo = DataStatisticsListAlgo[1::2]
        DataAlgo.insert(0,tag)

        print(len(ColumnNames))
        print(len(DataAlgo))

        ##Crate Empty Dataframe with 61 Columns
        #Add Columns and Data
        Stats.loc[len(Stats)] = DataAlgo

def IncomeStatement(tag):

        global IncomeStatementSummary
        element3 = driver.find_element(By.XPATH, '//ul[@class="List(n) Whs(nw) fin-tab-items W(100%) Lh(1.7) H(44px) Bdbs(s) BdB(4px) Cf Mb(15px) Bdbc($seperatorColor) "]/li[7]/a[1]')
        action = ActionChains(driver)
        action.click(on_element = element3)
        action.perform()
        time.sleep(5)

        #Get Income Common Stockholders 
        element4 = driver.find_element(By.XPATH, '//button[@aria-label="Net Income Common Stockholders"]')
        action = ActionChains(driver)
        action.click(on_element = element4)
        action.perform()
        time.sleep(5)


        ####Here we collect the income statement in full########
        dataIS = driver.find_elements(By.XPATH, '//div[contains(@class, "Ta(c) Py(6px) Bxz(bb) BdB Bdc($seperatorColor) Miw(120px) Miw(100px)--pnclg Bgc($lv1BgColor) fi-row:h_Bgc($hoverBgColor) D(tbc)") or contains(@class, "Ta(c) Py(6px) Bxz(bb) BdB Bdc($seperatorColor) Miw(120px) Miw(100px)--pnclg D(tbc)")]')
        column_headersIS = driver.find_elements(By.XPATH, '//div[contains(@class, "D(ib) Va(m) Ell Mt(-3px) W(215px)--mv2 W(200px) undefined") or contains(@class, "D(ib) Va(m) Ell Mt(-3px) W(200px)--mv2 W(185px) undefined")]')
        Dates = driver.find_elements(By.XPATH,  '//div[contains(@class, "Ta(c) Py(6px) Bxz(bb) BdB Bdc($seperatorColor) Miw(120px) Miw(100px)--pnclg D(ib) Fw(b) Tt(u) Bgc($lv1BgColor)") or contains(@class, "Ta(c) Py(6px) Bxz(bb) BdB Bdc($seperatorColor) Miw(120px) Miw(100px)--pnclg D(ib) Fw(b)")]')

        IncomeStatementHeadersAlgo = []
        IncomeStatementDataAlgo =[]
        DatesColumnAlgo=[]

        for value in column_headersIS:
             IncomeStatementHeadersAlgo.append(value.text)

        for value in dataIS:
             IncomeStatementDataAlgo.append(value.text)
     
        for value in Dates:
             DatesColumnAlgo.append(value.text)
     

        #print('Data --> {}'.format(len(dataIS)))
        print('ColumnHeaders --> {}'.format(len(column_headersIS)))

        ######Chunck size is len of Dates column
        chunk_sizeAlgo = len(DatesColumnAlgo)
        ListOfListsISAlgo = list()

        for i in range(0, len(IncomeStatementDataAlgo), chunk_sizeAlgo):
            ListOfListsISAlgo.append(IncomeStatementDataAlgo[i:i+chunk_sizeAlgo])
 
        IncomeStatementYearly = pd.DataFrame()
 
        #Add Rows with Chunk size
        for z in range(0, len(IncomeStatementHeadersAlgo), 1):
            IncomeStatementYearly[z] = ListOfListsISAlgo[z]


        IncomeStatementYearly.columns = IncomeStatementHeadersAlgo
        IncomeStatementYearly.insert(0, "tag", tag)
        IncomeStatementYearly.insert(1, "Dates", DatesColumn)

        IncomeStatementSummary = IncomeStatementSummary.append(IncomeStatementYearly, ignore_index=True)


####Here we collect the Balance Sheet in full########
def BalanceSheet(tag):
    global BalanceSheetSummary
            #Go to Balance Sheet
    BalanceSheetBtn = driver.find_element(By.XPATH, '//div[@class="Fw(500) D(ib) Pend(10px) H(18px) BdEnd Bdc($seperatorColor)"]')
    action = ActionChains(driver)
    action.click(on_element = BalanceSheetBtn)
    action.perform()
    time.sleep(5)

####Open subaccounts of BalanceSheet
    try:
        TotalAssetsBtn = driver.find_element(By.XPATH,  '//button[@aria-label="Total Assets"]')
        action = ActionChains(driver)
        action.click(on_element = TotalAssetsBtn)
        action.perform()
        time.sleep(0.2)

        TotalLiabilitiesBtn = driver.find_element(By.XPATH,  '//button[@aria-label="Total Liabilities Net Minority Interest"]')
        action = ActionChains(driver)
        action.click(on_element = TotalLiabilitiesBtn)
        action.perform()
        time.sleep(0.2)

        TotalEquityBtn = driver.find_element(By.XPATH,  '//button[@aria-label="Total Equity Gross Minority Interest"]')
        action = ActionChains(driver)
        action.click(on_element = TotalEquityBtn)
        action.perform()
        time.sleep(0.2)

    except NoSuchElementException:
        print("Element not found")


    try:
        dataBS = driver.find_elements(By.XPATH, '//div[contains(@class, "Ta(c) Py(6px) Bxz(bb) BdB Bdc($seperatorColor) Miw(120px) Miw(100px)--pnclg D(tbc)") or contains(@class, "Ta(c) Py(6px) Bxz(bb) BdB Bdc($seperatorColor) Miw(120px) Miw(100px)--pnclg Bgc($lv1BgColor) fi-row:h_Bgc($hoverBgColor) D(tbc)")]')
        DatesBS = driver.find_elements(By.XPATH,'//div[contains(@class, "Ta(c) Py(6px) Bxz(bb) BdB Bdc($seperatorColor) Miw(120px) Miw(100px)--pnclg D(ib) Fw(b)") or contains(@class, "Ta(c) Py(6px) Bxz(bb) BdB Bdc($seperatorColor) Miw(120px) Miw(100px)--pnclg D(ib) Fw(b) Bgc($lv1BgColor)")]' )
        column_headersBS = driver.find_elements(By.XPATH,'//div[contains(@class, "D(ib) Va(m) Ell Mt(-3px) W(215px)--mv2 W(200px) undefined") or contains(@class, "D(ib) Va(m) Ell Mt(-3px) W(200px)--mv2 W(185px) undefined")]' )


        #print('Data --> {}'.format(len(dataBS)))
        print('ColumnHeaders --> {}'.format(len(column_headersBS)))

        BalanceSheetDataAlgo = []
        BSColumnHeadersListAlgo =[]
        DatesBSListAlgo = []
    
        for value in  column_headersBS:
         BSColumnHeadersListAlgo.append(value.text)

        for value in dataBS:
         BalanceSheetDataAlgo.append(value.text)

        for value in DatesBS:
         DatesBSListAlgo.append(value.text) 

    
        ListOfListsBS = list()
        chunk_size_BS = len(DatesBSListAlgo)

        for i in range(0, len(BalanceSheetDataAlgo), chunk_size_BS):
            ListOfListsBS.append(BalanceSheetDataAlgo[i:i+chunk_size_BS])

        BalanceSheetYearly= pd.DataFrame()

        for z in range(0, len(BSColumnHeadersListAlgo), 1):
         BalanceSheetYearly[z] = ListOfListsBS[z]
    
        BalanceSheetYearly.columns = BSColumnHeadersListAlgo

        BalanceSheetYearly.insert(0, "tag", tag)
        BalanceSheetYearly.insert(1, "Dates", DatesBSList)

        BalanceSheetSummary = BalanceSheetSummary.append(BalanceSheetYearly, ignore_index=True)

    except NoSuchElementException:
        print("Element not found")
     #### End of Balance Sheet Collection ########


for tag in taglist:
    Statistics(tag)
    IncomeStatement(tag)
    BalanceSheet(tag)


Stats.to_excel("C:/Users/User/Desktop/Python/ScrapeYFinance/Stats.xlsx",
                 sheet_name='Sheet_name_1')  

IncomeStatementSummary.to_excel("C:/Users/User/Desktop/Python/ScrapeYFinance/IncomeStatementSummary.xlsx",
                 sheet_name='Sheet_name_1')  

BalanceSheetSummary.to_excel("C:/Users/User/Desktop/Python/ScrapeYFinance/BalanceSheetSummary.xlsx",
                 sheet_name='Sheet_name_1')  