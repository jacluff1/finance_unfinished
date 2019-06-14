# import external dependencies
import numpy as np
import pandas as pd
import pdb
import os
import matplotlib.pyplot as plt
import seaborn as sn

# import external dependencies
from Base import Base

# from matplotlib.ticker import FuncFormatter
# def hundreds(x, pos):
#     return '%2.0f' % (x * 1e-2)
# formatter = FuncFormatter(hundreds)

#===============================================================================
# kwargs
#===============================================================================

kwargs = {
    'csv_'      : {
        'map_rows_'     : 'AccountDataMapRows.csv',
        'raw_data_'     : 'ExportedTransactions.csv',
        'clean_data_'   : 'clean.csv',
    },
    'map_cols_' : {
        'ID'            : 'Reference Number',
        'amount'        : 'Amount',
        'description'   : 'Description',
        'category'      : 'Transactional Category'
    }
}

#===============================================================================
# class definition
#===============================================================================

class AccountData(Base):

    def __init__(self, **kwargs):
        super().__init__(kwargs)

        # load csv files
        for attr,file in self.csv_.items():
            setattr(self, attr, pd.read_csv(file))

        update_cleaned_data()

    def update_cleaned_data(self):

        # check if files are present
        raw_present = hasattr(self, 'raw_data_')
        clean_present = hasattr(self, 'clean_data')
        if not any([raw_present, clean_present]):
            print("There doesn't appear to be any raw or cleaned data present")
            return

        # alias column map
        colMap = self.map_cols_

        if clean_present:
            # alias clean data
            clean = self.clean_data_
            if raw_present:
                # alias raw data
                raw = self.raw_data_
                # rename columns in raw data
                
                # only select raw data that isn't in clean data
                raw = raw[ ~raw[colMap['ID']].isin(clean[self.meta_['ID']) ]
                # clean raw data and merge it with the already clean data
                clean = clean.append( self.__clean_raw_data(raw), ignore_index=True )
        elif raw_data:
            # clean raw data
            clean = self.__clean_raw_data( pd.read_csv(self.files_['raw_data']) )

        # save cleaned data
        self.clean_data_ = clean

    #===========================================================================
    # helper methods
    #===========================================================================

    def __clean_raw_data(self, raw):

        # only select useful columns
        raw = raw[self.meta['raw_columns']]

        # convert long data descriptions to shorter descriptions
        def apply_me

#===============================================================================
# load and clean data
#===============================================================================

def clean_raw():

    #===========================================================================
    # get data
    #===========================================================================

    data = pd.read_csv("data/ExportedTransactions.csv")

    # select useful columns
    data = data[['Posting Date', 'Amount', 'Description', 'Transaction Category']]

    for category,dictionary in categories.items():
        for description,new_description in dictionary.items():
            data.loc[data.Description.str.contains(description),"Transaction Category"] = category
            data.loc[data.Description.str.contains(description),"Description"] = new_description

    #===========================================================================
    # dates
    #===========================================================================

    dates = pd.DatetimeIndex(data['Posting Date'])
    data['year'] = dates.year
    data['month'] = dates.month
    data['day'] = dates.day

    periods = dates.to_period(freq='M')
    periods1 = np.empty(periods.shape[0], dtype=np.int32)
    for i,period in enumerate(periods.unique()):
        periods1[ periods == period ] = i
    data['period'] = periods1
    data['period_yr_m'] = periods

    data.drop('Posting Date', axis=1, inplace=True)

    #===========================================================================
    # rename columns
    #===========================================================================

    data.rename(str.lower, axis=1, inplace=True)
    data.rename(index=str, columns={'transaction category':'category'}, inplace=True)

    #===========================================================================
    # fill nans
    #===========================================================================

    data.category.fillna(value='misc', inplace=True)

    #===========================================================================
    # save
    #===========================================================================

    data.to_csv("private/clean.csv", index=False)

def load_data():
    return pd.read_csv("private/clean.csv")

#===============================================================================
# select portions of the data
#===============================================================================

def select_expenses(data):
    return data[data.amount < 0]

def select_income(data):
    return data[data.amount > 0]

def select_year(data,year):
    return data[data.year == year]

def select_month(data,month):
    return data[data.month == month]

def select_day(data,day):
    return data[data.day == day]

def select_period(data,period):
    return data[data.period == period]

def select_whole_periods(data):
    pmin = data.period.min()
    pmax = data.period.max()
    return data[(data.period > pmin) & (data.period < pmax)]

#===============================================================================
# find useful information from the data
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
