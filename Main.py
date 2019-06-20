# import external dependencies
import pandas as pd
import pdb

# import internal dependencies
import AccountData as ad
import Loans as ln
import Expenses as ex

#===============================================================================
# kwargs
#===============================================================================

ad_kwargs = {
    'csv_'      : {
        'map_rows_'     : 'AccountDataMap.csv',
        'raw_data_'     : 'ExportedTransactions.csv',
        'clean_data_'   : 'clean.csv'
    },
    'map_cols_' : {
        'ID'            : 'Reference Number',
        'amount'        : 'Amount',
        'description'   : 'Description',
        'date'          : 'Posting Date',
        'category'      : 'Transaction Category'
    }
}

ln_kwargs = {
    'csv_'                  : {
        'loans_'            : 'Loans.csv',
        'loan_priorities_'  : 'Loan_priorities.csv'
    },
    'house_'                : {
        'name'              : 'Home-Tucson',
        'balance'           : 68635.94,
        'sale_price'        : 180e3,
        'purchase_price'    : 300e3,
        'APR'               : 0.0422,
        'term'              : 30,
        'downpayment'       : .2,
        'tax_rate'          : 0,
        'closing_cost_rate' : 0.02,
        'realtor_rate'      : 0
    },
    'car_'                  : {
        'name'              : 'XLE-Rav4',
        'purchase_price'    : 29500,
        'APR'               : 0.0389,
        'term'              : 6,
        'downpayment'       : 1250 + 500 + 200,
        'tax_rate'          : 0.083,
        'doc_fee'           : 489,
        'plates'            : 544.22,
        'tire_tax'          : 5
    },
    'house_sale_proceeds_'  : {
        'savings'           : 9e3,
        'credit cards'      : 2400
    },
    'payments_'             : {
        'extra'             : 1000,
    },
    'JC_condensed_payment_' : 49.02,
}

ex_kwargs = {
    'csv_'      : {
        'expenses_' : 'Expenses.csv',
        'bills_'    : 'Bills.csv',
        'income_'   : 'Income.csv',
        'plan_'     : 'Planning.csv'
    },
}

def grid_search_options():
    # sync and map account data
    AccountData = ad.AccountData( **ad_kwargs )
    # create empty container to hold scenarios
    scenarios = []
    # grid search options for purchase price and extra payments on loans
    for purchase_price in [25e3*x for x in range(10,17)]:
        for extra in [100*x for x in range(6,11)]:
            # update kwargs
            ln_kwargs['house_']['purchase_price'] = purchase_price
            ln_kwargs['payments_']['extra'] = extra
            # calculate loans and expenses
            Loans = ln.Loans( **ln_kwargs )
            Expenses = ex.Expenses( Loans, **ex_kwargs )
            # get the indices for emergency savings and fun savings
            idx_map = Expenses.get_index_map(['emergency', 'fun'], df=Expenses.expenses_)
            # collect items of interest in DataFrame
            df = pd.DataFrame({
                'purchase_price'    : purchase_price,
                'extra_payment'     : extra,
                'house_payment'     : Loans.payments_['Home-Tucson'],
                'emergency'         : Expenses.expenses_.loc[ idx_map['emergency'], 'amount' ],
                'fun'               : Expenses.expenses_.loc[ idx_map['fun'], 'amount' ]
            }, index=[0])
            # if emergency (or fun) is positive, include it in scenarios
            if df.emergency.item() > 0: scenarios.append(df)
    # combine all the scenarios into a single DataFrame
    scenarios = pd.concat(scenarios, ignore_index=True, sort=False)
    # set savings goals
    emergency_goal = pd.read_csv("Income.csv").net.item() * 6
    fun_goal = 10e3
    # calculate columns to describe how many months to reach a goal
    scenarios['months till emergency goal'] = emergency_goal / scenarios.emergency
    scenarios['months till fun goal'] = fun_goal / scenarios.fun
    # save scenarios to csv
    scenarios.to_csv("Scenarios.csv", index=False)
    print(scenarios)

def main():
    AccountData = ad.AccountData( **ad_kwargs )
    Loans = ln.Loans( **ln_kwargs )
    cash = Loans.cash_ # money left after selling house and paying off loans
    Expenses = ex.Expenses( Loans, **ex_kwargs )

#===============================================================================

if __name__ == '__main__':

    grid_search_options()
    # main()
