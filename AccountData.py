# import external dependencies
import numpy as np
import pandas as pd
import os
# import matplotlib.pyplot as plt
# import seaborn as sn
# from matplotlib.ticker import FuncFormatter
# def hundreds(x, pos):
#     return '%2.0f' % (x * 1e-2)
#     formatter = FuncFormatter(hundreds)

# import external dependencies
from Base import Base

#===============================================================================
# selection functions
#===============================================================================

def select_expenses(data):
    return data[data.amount < 0]

def select_income(data):
    return data[data.amount > 0]

def select_year(data, year):
    return data[data.year == year]

def select_month(data, month):
    return data[data.month == month]

def select_day(data, day):
    return data[data.day == day]

def select_period(data, period):
    return data[data.period == period]

def select_whole_periods(data):
    pmin = data.period.min()
    pmax = data.period.max()
    return data[(data.period > pmin) & (data.period < pmax)]

#===============================================================================
# find useful information from data
#===============================================================================

def N_per(data):
    return data.period.unique().shape[0]

def find_monthly_income(data):
    income = select_income(data)
    Nperiods = income.period.unique().shape[0]
    return income.groupby('period_yr_m').amount.sum()

def find_monthly_expenses(data):
    expenses = select_expenses(data)
    Nperiods = expenses.period.unique().shape[0]
    return expenses.groupby('period_yr_m').amount.sum().abs()

def find_monthly_profits(data):
    income = find_monthly_income(data)
    expenses = find_monthly_expenses(data)
    return income - expenses

def find_average_income(data):
    result = select_income(data).amount.to_numpy(dtype=np.float32).sum() / N_per(data)
    return round(result,2)

def find_average_expenses(data):
    result = select_expenses(data).amount.to_numpy(dtype=np.float32).sum() / N_per(data)
    return round(result,2)

def find_average_profits(data):
    result = find_monthly_profits(data).sum() / N_per(data)
    return round(result,2)

def find_ambers_average_income(data):

    # select data
    amber = data[(data.description == 'Private Clients') | (data.description == 'Cash Withdrawal') | (data.description == 'Envy') | (data.description == 'Cortiva')]

    return int(amber.amount.to_numpy(dtype=np.float32).sum() / N_per(data))

#===============================================================================
# plots and figures
#===============================================================================

def plot_expense_categories(data):

    # get expense data
    expenses = select_expenses(data).groupby('category').amount.sum().abs().sort_values(ascending=False)

    # set up figure
    fig,ax = plt.subplots(ncols=2, figsize=(20,10))
    fig.suptitle("Expenses by Category", fontsize=25)

    # plot pie chart
    ax[0].pie(expenses.values, labels=expenses.index.values, autopct='%1.1f%%')

    # plot bar graph
    ax[1].yaxis.set_major_formatter(formatter)
    ax[1].set_ylabel("\$ [hundreds]", fontsize=20)
    x = np.arange(expenses.shape[0])
    ax[1].bar(x,expenses.values)
    ax[1].set_xticks(x)
    ax[1].set_xticklabels(expenses.index, rotation=45, fontsize=10)

    plt.tight_layout()
    plt.subplots_adjust(wspace=.15, bottom=.15, top=.9)

    # save and close
    fig.savefig("private/expense_categories.pdf")
    plt.close(fig)

def plot_profits(data):

    profits = find_monthly_profits(data)
    x = np.arange(profits.shape[0])

    fig,ax = plt.subplots()

    ax.bar(x, profits.values)
    ax.set_xticks(x)
    ax.set_xticklabels(profits.index, rotation=90, fontsize=10)
    ax.set_xlabel("Month", fontsize=15)
    ax.set_ylabel("Profit [hundreds]", fontsize=15)
    ax.yaxis.set_major_formatter(formatter)

    plt.tight_layout()
    plt.subplots_adjust(bottom=.2, top=.9)

    fig.savefig("private/monthly_profits.pdf")
    plt.close(fig)

#===============================================================================
# class definition
#===============================================================================

class AccountData(Base):

    def __init__(self, **kwargs):
        print("\nconstructing AccountData instance...")
        self.name_ = "AccountData"
        super().__init__(**kwargs)

        self.update_cleaned_data()
        self.save_csv('clean_data_')
        # self.print_self()

    def update_cleaned_data(self):

        print("\nupdating cleaned data")

        # check if files are present
        raw_present = hasattr(self, 'raw_data_')
        clean_present = hasattr(self, 'clean_data_')
        if not any([raw_present, clean_present]):
            print("There doesn't appear to be any raw or cleaned data present")
            return

        if clean_present:
            # alias clean data
            clean = self.clean_data_
            if raw_present:
                # alias raw data
                raw = self.raw_data_
                # only select raw data that isn't in clean data
                raw = raw[ ~raw[self.map_cols_['ID']].isin(clean['ID']) ]
                # clean raw data and merge it with the already clean data
                clean = clean.append( self.__clean_raw_data(raw), ignore_index=True )
                # delete raw data file
                os.remove( self.csv_['raw_data_'] )
        elif raw_present:
            # clean raw data
            clean = self.__clean_raw_data( self.raw_data_ )

        # save cleaned data
        self.clean_data_ = clean

    #===========================================================================
    # helper methods
    #===========================================================================

    def __clean_raw_data(self, raw):

        print("\ncleaning raw data...")

        # rename columns in raw data
        raw = raw.rename(columns={val:key for key,val in self.map_cols_.items()})

        # only select useful columns
        raw = raw[ [*self.map_cols_] ]

        #=======================================================================
        # relabel data
        #=======================================================================

        # convert long data descriptions to shorter descriptions
        for i in range(self.map_rows_.shape[0]):
            # select row from map_rows_ DF
            row = self.map_rows_.iloc[i]
            # filter to select rows from raw data
            mask = raw.description.str.contains( row.search_key )
            # rename description and category
            raw.loc[mask,'description'] = row.new_description
            raw.loc[mask,'category'] = row.category

        #===========================================================================
        # dates
        #===========================================================================

        dates = pd.DatetimeIndex(raw.date)
        raw['year'] = dates.year.values.astype(np.int32)
        raw['month'] = dates.month.values.astype(np.int32)
        raw['day'] = dates.day.values.astype(np.int32)

        raw['period_yr_m'] = dates.to_period(freq='M')
        periods = np.empty(raw.shape[0], dtype=np.int32)
        for i,period in enumerate(raw.period_yr_m.unique()):
            periods[ raw.period_yr_m == period ] = i
        raw['period'] = periods

        raw.drop('date', axis=1, inplace=True)

        #=======================================================================
        # fill nans
        #=======================================================================

        raw.category.fillna(value='misc', inplace=True)

        #=======================================================================
        # output
        #=======================================================================

        return raw
