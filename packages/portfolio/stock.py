"""
stock --> collects investment data of companies from yahoo finance.
"""
from re import U
import pandas as pd
import datetime as dt 
import os
import json

from yfinance import Ticker
from currency_converter import CurrencyConverter


class Stock(Ticker):
    
    def __init__(self, ticker, displayCurrency="ZAR", baseSaveDirectory=os.path.normpath("./"), isJSE=False, *args, **kwargs):
        super(Stock, self).__init__(ticker, *args, **kwargs)

        # Base directory for the stock data saves
        self.baseStockDataDirectory = os.path.normpath(os.path.join(baseSaveDirectory, self.ticker))

        # Base directory of the Financial Statements of the stock
        self.baseStockFinancialStatementsDirectory = os.path.join(self.baseStockDataDirectory, "FinancialStatements")

        # Directory for the Cashflow, BalanceSheet and income Statements of the stock 
        self.cashflowSaveDirectory = os.path.join(self.baseStockFinancialStatementsDirectory,"cashflow") 
        self.incomestatementSaveDirectory = os.path.join(self.baseStockFinancialStatementsDirectory, "incomestatement")
        self.balancesheetSaveDirectory = os.path.join(self.baseStockFinancialStatementsDirectory, "balancesheet")

        # display currency, default to ZAR
        self.__displayCurrency = displayCurrency
        self.currencyConverter = CurrencyConverter()

		# Determines whether the stock data requires JSE Yahoo correction or not
        self.isJSE = isJSE

        # List of the available keys to the clean info data
        self.cleanInfoKeys = ['sector', 'zip', 'fullTimeEmployees', 'longBusinessSummary', 'city', 'phone', 'country', 'website', 'address1', 'address2', "fax", "industry", "recommendationKey", "financialCurrency", "exchange", "shortName", "longName", "exchangeTimezoneName", "symbol", "logo_url"]

        # Stock info file
        self._StockInfoFilePath = os.path.join(self.baseStockDataDirectory, "StockInfo.json")

    @property
    def __stock_purchase_history(self) -> pd.DataFrame:
        """
            This function will return a pandas data frame object of the details about the purchases made to the stock
        """
        pass
    
    @property
    def purchaseValue(self) -> float:
        """
            This function will return the total sum of money invested into the stock
        """
        pass

    @property
    def shares(self) -> float:
        """
            This function will return the number of shares owned in the company
        """

    @property
    def nextDividendsDate(self) -> dt.datetime:
        """
            returns the date of the next dividends payout date
        """

    @property
    def saveCashFlow(self):
        """
            Saves the cash flow statement of the stock in a csv or json file
        """

    @property
    def saveBalanceSheet(self):
        """
            Saves the Balance sheet of the stock in a csv or json file
        """

    @property
    def saveIncomeStatement(self):
        """
            Saves the income statement of a stock in a csv or json file
        """

    @property
    def returnOnInvestment(self) -> float:
        """
            returns the profit/loss of the investment relative to your purchase
        """

    @property
    def financial_analysis(self) -> dict:
        """
            returns the financial analysis of the stock based on the latest yearly financial statement
        """

    @property
    def quarterly_financial_analysis(self) -> dict:
        """
            returns the financial analysis of the stock based on the latest quarterly financial statement
        """

    def cleanInfo(self, updated: bool=False) -> dict:
        """
            (args) updated: determines whether to return stored data or get new data from api
            gets useful info about the stock
        """

        if updated:
            # Returning current data from yahoo, if updated is true
            info = self.info
            return { key:info[key] for key in self.cleanInfoKeys}

        elif os.path.exists(self._StockInfoFilePath):
            # Returning the stored data, if updated is false
            with open(self._StockInfoFilePath, 'r') as file:
                data = json.load(file)

            return data
        
        else:
            # Returning current data if folder was not found
            info = self.info
            return { key:info[key] for key in self.cleanInfoKeys}
 
    def loadDirectories(self):
        """
            Responsible for loading the required directories into memory
        """

        # Getting the keys to directory based attributes
        directoryAttributeKeys = [x for x in self.__dict__.keys() if x.endswith("Directory")]

        # Creating the directories 
        for key in directoryAttributeKeys:
            # Checking if folder already exist
            if not os.path.exists(self.__dict__[key]):
                os.makedirs(self.__dict__[key])

    def __JSE_YAHOO_CORRECTION(self, stockHistory):
        """
            Corrects the price data of JSE stocks from yahoo finance
        """
        # Correcting Open price data
        stockHistory['Open'] = [x*10**-2 for x in stockHistory['Open']]

        # Correcting High price data
        stockHistory['High'] = [x*10**-2 for x in stockHistory['High']]

        # Correcting Low price data
        stockHistory['Low'] = [x*10**-2 for x in stockHistory['Low']]

        # Correcting Close price data
        stockHistory['Close'] = [x*10**-2 for x in stockHistory['Close']]

        return stockHistory

    def history(self, *args, **kwargs):
        if(self.isJSE):
            return self.__JSE_YAHOO_CORRECTION(super().history(*args, **kwargs))
        else:
            return super().history(*args, **kwargs)

    def saveCleanInfo(self, destination: str=None) -> bool:
        """
            (args) destination: defines the directory that the stock info will be stored in, defaults to the baseStockDataSaves
            saves the useful data about the stock in a json file in the base directory of the stock
        """

        # Confirming the destination of the directory
        destination = destination if not destination else self.baseStockDataDirectory

        # Creating the data storage variable
        info = self.info
        cleanInfo = { key:info[key] for key in self.cleanInfoKeys}

        # Storing the data into json file
        with open(self._StockInfoFilePath, 'w') as file:
            json.dump(cleanInfo, file, indent=4)

        return os.path.exists(self._StockInfoFilePath)

    def graphStock(self, save: bool = False, show: bool = True, directory = None, *args, **kwargs):
        """
        arg: save -> bool: determines whether the graph will be saved to storage, defaults to false
        arg: show -> bool: determines whether the graph will be displayed or not, defaults to true
        arg: directory: the directory that the graph is going to be saved in, defaults to the stock's base directory

        This function graphs the price of the stocks for specific periods and intervals
        """
    
    def isCurrentPriceAvgDiscount(self, discount) -> bool:
        """
        arg: discount: a float that will be used to determine the criteria

        check whether the current price of the stock is a discount relative to the average purchase price you made towards the stock
        """
    
    def buyStock(self, dateOfpurch: dt.datetime, purchasePrice: int=0, stocksPurch: int=0, purchaseCurrency: str=None, save: bool=True):
        """
            (args) purchasePrice: the money spent on a specific date to buy stock(s)
            (args) dateOfpurch: the date at which the stock was bought, datetime object
            (args) stocksPurch: the number of stocks purchased on the date
            (args) purchaseCurrency: the currency used to purchase the stock, defaults to displayCurrency

            if purchasePrice is'nt provided the function will use the stockspurch value and the date of puchase to estimate
            how much you own and if the stockspurch is not provided the funtion will use the purchaseprice and date of puchase to estimate
            how many stocks you own.

            Updates the purchase history of the stock, by storing the date of purchase of the stock and its price on that date, as well as the number of stocks bought and the price paid for that quantity.
        """

        # Raise an ValueError if both stocksPurch and purchasePrice is not given

        # Confirming the purchase currency

        # Acquire the stock price of the stock on the given date

        # Calculating the purchase price of the stock if it is not given

        # Calculating the stocks purchases if it is not given

        # Store the data in to the stocks purchase history json table



if __name__ == '__main__':
    tsla = Stock("CPI.JO", isJSE=True, baseSaveDirectory="C:/Users/lelet/Desktop(offline)/Personal Finacial Records/InvestmentPortfolio/InvestementTracker/AgentFinance")