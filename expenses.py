# import libraries
import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import os
import pdb

class expenses:

    def __init__(self):
        print("\nInitializing expenses instance...")
        print("collecting filenames...")
        filename            =   {}
        filename['DF']      =   "data/DF_data.csv"
        self.__filename     =   filename
        self.__data         =   self.GET_DATA()

    #===============================================================================================
    # puplic methods
    #===============================================================================================

    def GET_DATA(self):
        if os.path.isfile(self.__filename['DF']):
            print("loading data from file")
            self.__LOAD_DATA()
        else:
            df              =   bank.bank()
            self.__data     =   bank.GET_DATA()
            self.__ADD_TIME_COLUMNS()
        return self.__data

    #===============================================================================================
    # private methods
    #===============================================================================================

    def __LOAD_DATA(self):
        print("loading Desert Finantial data...")
        self.__data     =   pd.read_csv(self.__filename['DF'], index_col='Unnamed: 0')
        self.__ADD_TIME_COLUMNS()

    def __ADD_TIME_COLUMNS(self):
        data                =   self.__data
        data['datetime']    =   pd.to_datetime(data['Posting Date'])
        data['year']        =   data.apply(lambda x: x['datetime'].year, axis=1)
        data['month']       =   data.apply(lambda x: x['datetime'].month, axis=1)
        start               =   data.datetime.min()
        data['period']      =   data.apply(lambda x: x['datetime'].to_period('M') - start.to_period('M'), axis=1)
        self.__data         =   data.sort_values("datetime")

    def __GET_CURRENT_MONTH(self):
        NotImplemented

    def GET_MONTHLY_VALUES_FROM_DATA(self,search_key,index_i,index_f):
        data            =   self.__data
        # values          =   data[data.Description.str.contains(search_key)].Amount.values[index_i:index_f]
        if values.shape[0] == 1:
            return values[0]
        else:
            return values

    def GET_PLANNED_EXPENSES(self,datetime):
        data                        =   self.__data
        exp                         =   {}
        exp['ds-card']              =   self.GET_MONTHLY_VALUES_FROM_DATA("CARDMEMBER",-2,-1)
        exp['mortgage']             =   self.GET_MONTHLY_VALUES_FROM_DATA("CARRINGTON",-2,-1)
        exp['car insurnace']        =   self.GET_MONTHLY_VALUES_FROM_DATA("SAFECO",-2,-1)
        exp['solar city']           =   self.GET_MONTHLY_VALUES_FROM_DATA("SOLAR CITY",-2,-1)
        exp['priusV']               =   -351.43
        exp['Mesa-utilities']       =   np.average(self.GET_MONTHLY_VALUES_FROM_DATA("CITY OF MESA",0,-1).values)
        # exp['Navient-Amber']        =
        # exp['Navient-Jacob']        =
        # exp['Primerica']            =
        # exp['Netflix']              =
        # exp['SRP']                  =
        # exp['Spotify']              =
        exp['CenturyLink']          =   self.GET_MONTHLY_VALUES_FROM_DATA("CENTURYLINK",-2,-1)
        # exp['gas']                  =
        # exp['other']                =
        # exp['car-maintenance']      =
        # exp['registration']         =
        # exp['massage-insurance']    =
        # exp['Prime']                =

        # gas
        # other

        # car maintencance
        # vehicle registration
        # massage insurance
        # amazon
