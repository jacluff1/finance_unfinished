# import libraries
import dataCollection
import pandas as pd

class income:

    def __init__(self,**kwargs):
        print("\nstarting planned income...")
        self.__hours    =   dataCollection.GOOGLE_CALENDAR(**kwargs)
        self.__envy     =   dataCollection.MASSAGE_ENVY(**kwargs)
        self.__ADD_HOURS()
        self.__ADD_RATES()
        self.__ADD_NET_PERCENTAGES()
        self.__ADD_PLANNED_INCOME()
        self.__SAVE_DATA()
        print("finished creating planned_income instance.")

    def __ADD_HOURS(self):
        print("adding hours...")
        data                =   pd.read_csv("hours_data.csv", index_col='Unnamed: 0')
        data['datetime']    =   pd.to_datetime(data.weekdate)
        self.data           =   data

    def __ADD_RATES(self):
        print("adding gross pay rates...")
        self.data['EnvyRate']       =  self.data.apply(lambda x: self.__envy.GET_PAY_RATE(x['weekdate']), axis=1)
        self.data['CortivaRate']    =   18

    def __ADD_NET_PERCENTAGES(self):
        print("adding net percentages...")
        self.data['EnvyNetP']       =   self.__envy.GET_NET_PERCENTAGE()
        self.data['CortivaNetP']    =   439.75/504

    def __ADD_PLANNED_INCOME(self):
        print("calculating planned income...")
        self.data['EnvyNet']        =   self.data.EnvyHours * self.data.EnvyRate * self.data.EnvyNetP
        self.data['CortivaNet']     =   (self.data.CortivaHours*self.data.CortivaRate + 3*12) * self.data.CortivaNetP
        self.data['NetIncome']      =   self.data.EnvyNet + self.data.CortivaNet

    def __SAVE_DATA(self):
        print("saving data to 'planned_income_data.csv'...")
        self.data.to_csv("planned_income_data.csv")
