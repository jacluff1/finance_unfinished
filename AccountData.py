import numpy as np
import pandas as pd
import pdb
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt

from matplotlib.ticker import FuncFormatter
def hundreds(x, pos):
    return '%2.0f' % (x * 1e-2)
formatter = FuncFormatter(hundreds)

#===============================================================================
# load and clean data
#===============================================================================

def clean_raw():

    #===========================================================================
    # get data
    #===========================================================================

    data = pd.read_csv("ExportedTransactions.csv")

    # select useful columns
    data = data[['Posting Date', 'Amount', 'Description', 'Transaction Category']]

    #===========================================================================
    # categories
    #===========================================================================

    bills = {
        'AHCCCSPREMBILL'        : 'AHCCCS - Kids Care',
        'BANK OF AMERICA ONLINE PMT': 'BoA - card',
        'BK OF AMER VISA'       : 'BoA - card',
        'CARDMEMBER'            : 'DF-card',
        'CARRINGTON'            : 'Carrington',
        'CENTURYLINK'           : 'CenturyLink',
        'CITY OF MESA CHECKPYMT': 'Mesa Utilities',
        'NAVI ED SERV PP STUDNTLOAN ACH TRANSACTION JAC'    : 'student loans - Jacob',
        'NAVI ED SERV PP STUDNTLOAN ACH TRANSACTION CLUFF'  : 'student loans - Amber',
        'NAVI ED SERV WEB STUDNTLOAN ACH TRANSACTION AM'    : 'student loans - Amber',
        'PLANET FIT'            : 'Planet Fitness',
        'SOLARCITY'             : 'Solar City',
        'SOLAR CITY'            : 'Solar City',
        'SRP SUREPAY'           : 'SRP',
        'T-MOBILE'              : 'Tmobile',
        'TRANSFER TO 2102'      : 'Prius V',
        }

    entertainment = {
        'AMC ONLINE'            : 'AMC',
        'ATOM TICKETS'          : 'Atom Tickets',
        'BLACKROCKCO'           : 'Blackrock Coffee',
        'DAIRY QUEEN'           : 'Dairy Queen',
        'EDIBLE ARRANGEMENTS'   : 'Edible Arrangements',
        'JAMBA JUICE'           : 'Jamba Juice',
        'JARRODS COFFEE TEA'    : 'Jarrods Coffee & Tea',
        'SPOTIFY'               : 'Spotify',
        'NETFLIX.COM'           : 'Netflix',
        'REDBOX'                : 'Redbox',
        'PLAYSTATION NETWORK'   : 'Playstation',
        'TOTAL WINE'            : 'Total Wine',
        'TICKETMASTER'          : 'Ticketmaster',
        'WORLD MARK THE CLUB'   : 'World Mark'
        }

    fees = {
        'AZ MOTOR VEHICLE'      : 'MVD',
        'AZ VEHICLE EMISSION'   : 'emissions',
        'PAID NSF FEE'          : 'Overdraft'
        }

    foodAndGrocery = {
        'ARBYS'                 : 'Arbys',
        'BACKYARD TACO'         : 'Backyard Taco',
        'BANNER DESERT BISTR'   : 'Banner Desert Bistro',
        'CHICK-FIL-A'           : 'Chick-Fil-A',
        'CHIPOTLE'              : 'Chipotle',
        'COSTCO'                : 'Costco',
        'CULINARY DROPOUT'      : 'Culinary Dropout',
        "DENNY'S"               : 'Dennys',
        'EL POLLO LOCO'         : 'El Pollo Loco',
        'FOOD CITY'             : 'Food City',
        'FRYS-MKTPLACE'         : 'Frys',
        'GENOS GIANT SLICE'     : 'Genos Pizza',
        'GO PUFF'               : 'Go Puff',
        'IN N OUT BURGER'       : 'In-N-Out',
        'LITTLE CAESARS'        : 'Little Caesars',
        'JIMMY JOHNS'           : 'Jimmy Johns',
        'MSB MESA UNIFIED'      : 'school lunches',
        'PANDA EXPRESS'         : 'Panda Express',
        'PRIME NOW'             : 'Prime Now',
        'PUBLIX'                : 'Publix',
        'RAISING CANES'         : 'Raising Canes',
        'SCHLOTZSKY'            : "Schlotzsky's",
        'SMART AND FINAL'       : 'Smart & Final',
        'SQ *'                  : 'SQ',
        'SUBWAY'                : 'Subway',
        'TACO BELL'             : 'Taco Bell',
        'TACO NAZO'             : 'Taco Nazo',
        'TACO PRADO'            : 'Taco Prado',
        'TARGET'                : 'Target',
        'WINCO FOODS'           : 'Winco',
        'WAL-MART'              : 'Wal-Mart',
        'WM SUPERCENTER'        : 'Wal-Mart'
        }

    health = {
        'WALGREENS'             : 'Walgreens',
        'AZ DEPT HLTH SVCS'     : 'Arizona Dept Health Services'
    }

    income = {
        'ARIZONA STATE'         : 'ASU',
        'CASH DEPOSIT'          : 'Private Clients',
        'CASH WITHDRAWAL'       : 'Cash Withdrawal',
        'CASH AND CHECK DEPOSIT': 'Envy',
        'DEPOSIT'               : 'Private Clients',
        'DEPOSIT CHECK'         : 'Envy',
        'FCNH'                  : 'Cortiva',
        'STRIPE TRANSFER X'     : 'Lyft',
        'TECHFIELD'             : 'Techfield'
        }

    insurance = {
        'PRIMERICA'             : 'Primerica',
        'SAFECO INSURANCE'      : 'Safeco'
        }

    investments = {
        'VANGUARD EDI PYMNTS'   : 'Vanguard Investments',
        'VGI-TGTRET2045 INVESTMENT' : 'Vanguard Investments'
        }

    shopping = {
        'AMAZON.COM'            : 'Amazon',
        'AMZN'                  : 'Amazon',
        'BLACK MARKET MINERA'   : 'Black Market Minera',
        'COSMOPROF'             : 'Cosmoprof',
        'CARTERS'               : 'Carters',
        'THE HOME DEPOT'        : 'Home Depot',
        'JOANN'                 : 'Joanns',
        'JOURNEYS KIDZ'         : 'Journeys Kidz',
        'KOHLS'                 : 'Kohls',
        'OFFICE MAX'            : 'Office Max',
        'PARTY CITY'            : 'Party City',
        'VISTAPRINT'            : 'Vistaprint'
        }

    transportation = {
        'ARCO'                  : 'Arco',
        'AUTO AIR & VACUUM'     : 'carwash',
        'CIRCLE K'              : 'Circle K',
        'EARNHARDT TOYOTA'      : 'Earnhardt',
        'LYFT'                  : 'Lyft',
        'RACEWAY CARWASH'       : 'carwash',
        'QT'                    : 'Quicktrip',
        'QUIKTRIP'              : 'Quicktrip',
        'SKYHARBORPARKINGTER'   : 'airport',
        'SHELL OIL'             : 'Shell Oil',
        'UBER'                  : 'Uber',
        }

    #===========================================================================
    # rename and categorize
    #===========================================================================

    categories = {
        'bills'             : bills,
        'fun'               : entertainment,
        'food & grocery'    : foodAndGrocery,
        'health'            : health,
        'income'            : income,
        'insurance'         : insurance,
        'investments'       : investments,
        'shopping'          : shopping,
        'transportation'    : transportation
        }

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

    data.to_csv("clean.csv", index=False)

def load_data():
    return pd.read_csv("clean.csv")

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
    # df = select_whole_periods(data)
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
    return round(result,2
    )

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
    fig.savefig("expense_categories.pdf")
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

    fig.savefig("monthly_profits.pdf")
    plt.close(fig)
