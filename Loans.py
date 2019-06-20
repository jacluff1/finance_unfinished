# import external dependencies
import pandas as pd
import numpy as np
import pdb

# import internal dependencies
from Base import Base
from Purchase import House, Car

#===============================================================================
# loan functions
#===============================================================================

def monthly_payment(balance0, APR, term):
    MPR = APR / 12
    n_per = term * 12
    F = (1 + MPR)**n_per
    return balance0 * MPR * F / (F - 1)

def monthly_interest_payment(balance, APR):
    return balance * APR/12

def monthly_principle_payment(payment, interest):
    return payment - interest

#===============================================================================
# payment functions
#===============================================================================

def make_minimum_payment(df, idx):
    payment = df.loc[idx,'payment']
    balance = df.loc[idx,'balance']
    APR = df.loc[idx,'APR']
    # calculate interest and principle payments
    interest = monthly_interest_payment(balance, APR)
    if balance < payment:
        principle = balance
    else:
        principle = monthly_principle_payment(payment, interest)
    # update df columns
    df.loc[idx,'interest'] += interest
    df.loc[idx,'principle'] += principle
    df.loc[idx,'payment_temp'] = interest + principle

def make_extra_payment(df, idx, extra):
    # pull the balance
    balance = df.loc[idx,'balance']
    # if the balance is greather than the available funds, make entire extra payment on loan
    if balance > extra:
        df.loc[idx,'balance'] -= extra
        extra = 0
    # if the available amount is greater than the balance, pay off the loan
    else:
        extra -= balance
        df.loc[idx,'balance'] = 0
    # output the extra available (0 > x > extra_available)
    return extra

def make_extra_payments(df, extra):
    # get the indices of the non-zero balanced loans
    indices = df[df.balance > 0].index.values
    # make extra payments with available funds, output any amount of extra left over
    for idx in indices:
        extra_available = make_extra_payment(df, idx, extra)
        if extra == 0: break
    return extra

#===============================================================================
# purchase functions
#===============================================================================

def purchase(df, purchase_instance):
    df1 = pd.DataFrame({
        'name'      : purchase_instance.name,
        'balance'   : purchase_instance.balance0,
        'payment'   : purchase_instance.payment,
        'APR'       : purchase_instance.APR
    }, index=[0])
    df = df.append(df1, ignore_index=True, sort=False)
    return df

#===============================================================================
# class definition
#===============================================================================

class Loans(Base):

    def __init__(self, **kwargs):
        print("\nconstructing Loans instance...")
        self.name_ = "Loans"
        super().__init__(**kwargs)

        self.__purchase_car()
        self.__purchase_house()
        self.__assign_priority_list()
        self.__apply_cash_from_selling_house_to_loans()

        # add the new minimum payments of remaining loans
        self.payments_.update( self.__collect_new_loan_setup() )

        # self.print_self()

    def __purchase_house(self):

        print(f"\npurchasing {self.house_['name']}...")

        # instantiate House
        house = House( **self.house_ )
        # add house to the loans
        self.loans_ = purchase(self.loans_, house)

        # add Mesa house balance and downpayment on new house to house_sale_proceeds_
        self.house_sale_proceeds_.update({
            'pay off Mesa house'        : house.balance,
            'downpayment on new house'  : house.downpayment,
        })

        # report on how sale proceeds will be used
        print("\nHow the proceeds from selling the house will be directed.")
        for key,value in self.house_sale_proceeds_.items():
            print(f"{value:0.2f}: \t {key}")

        # sum up redirected values from selling the house
        redirected = sum( self.house_sale_proceeds_.values() )

        # cash left to pay off loans
        self.cash_ = house.sale_price - redirected
        print(f"use ${self.cash_:0.2f} towards paying off loans.")

    def __purchase_car(self):

        print(f"\npurchasing {self.car_['name']}...")

        # instantiate Car
        car = Car( **self.car_ )
        # add car to loans
        self.loans_ = purchase(self.loans_, car)

    def __condense_student_loans(self, df):

        print("\ncondensing student loans...")

        # create filter for Jacob's student loans
        Jmask = df.name.str.contains("Jacob")
        # create separate DF for Jacob's student loans
        jacob = df[Jmask]

        # create filter for Amber's student loans
        Amask = df.name.str.contains("Amber")
        # create separate DF for Amber's student loans
        amber = df[Amask]
        # pdb.set_trace()

        # drop jacob's student loans from df
        df = df[ ~(Jmask | Amask) ]
        # create a new DataFrame of condensed Jacob Student Loans
        condensed = pd.DataFrame({
            'name'      : ['Student Loans-Jacob', 'Student Loans-Amber'],
            'balance'   : [jacob.balance.sum(), amber.balance.sum()],
            'payment'   : [self.JC_condensed_payment_, amber.payment.sum()]
        }, index=[0,1])
        # merge df and condensed
        df = df.append(condensed, ignore_index=True, sort=False)

        return df

    def __assign_priority_list(self):

        print("\nprioritizing loans payoffs...")

        # make a copy of loans
        df = self.loans_.copy()

        df = self.__condense_student_loans(df)

        # assign priorities
        df['priority'] = np.ones(df.shape[0], dtype=np.float32) *3
        for i in range(df.shape[0]):
            if df.loc[i,'name'] == 'Home-Mesa':
                df.loc[i,'priority'] = 1.0
            elif "Student Loans" in df.loc[i,'name']:
                df.loc[i,'priority'] = 2.0
            else:
                df.loc[i,'priority'] += (df.loc[i,'balance']/df.balance.sum()) / (df.loc[i,'payment']/df.payment.sum())

        # round
        for key in ['balance', 'payment', 'priority']:
            df[key] = df[key].round(2)

        # sort
        df = df.sort_values('priority')

        # reindex
        df.reset_index(drop=True, inplace=True)

        # assign and save
        self.loan_priorities_ = df
        self.save_csv( 'loan_priorities_' )

    def __apply_cash_from_selling_house_to_loans(self):

        print("\npaying off loans using extra money from selling the house...")

        # alias
        df = self.loan_priorities_
        cash = self.cash_

        # create new column to denote if loan is paid off
        df['paidoff'] = np.zeros(df.shape[0]) > 0

        # mark Home-Mesa as paid off
        df.loc[0,'paidoff'] = True

        # go through following loans and pay off what is possible
        print("\nchecking loans to payoff")
        for i in range(1,df.shape[0]):
            balance = df.loc[i,'balance']
            print(f"name: {df.loc[i,'name']} \t balance: {df.loc[i,'balance']} \t cash: {cash:0.2f}")
            if cash > balance:
                df.loc[i,'paidoff'] = True
                cash -= balance
            else:
                continue

        # select loans that have been paid off
        df1 = df[df.paidoff == True]

        # print results
        print("\npayoff results:")
        for i in df1.index:
            print(f"used ${df1.loc[i,'balance']} to pay off {df1.loc[i,'name']}.")
        print(f"have ${cash:0.2f} left over.")

        # assign and save
        self.loan_priorities_ = df
        self.cash_ = cash
        self.save_csv( 'loan_priorities_' )

    def __collect_new_loan_setup(self):
        payments = {}
        df = self.loan_priorities_[self.loan_priorities_.paidoff == False]
        df.reset_index(drop=True, inplace=True)
        for idx in range(df.shape[0]):
            payments[ df.loc[idx,'name'] ] = df.loc[idx,'payment']
        return payments

    def check_scenario(self):

        # make a copy of the loans DF
        df = self.loans_.copy()

        # add empty columns for interest and principle payments & current month's payment
        for key in ['interest', 'principle', 'payment_temp']:
            df[key] = np.zeros(df.shape[0], dtype=np.float32)

        # initialize variable for month counter
        m,total_balance = 0,self.total_balance_.copy()

        # make payments until the total balance = 0
        while total_balance > 0:

            if m % 5: print(f"month {m}")

            # find indices for loans with non-zero balances
            non_zero_idx = df[df.balance > 0].index.values
            # make minimum payments on all non-zero loans
            for idx in non_zero_idx:
                make_minimum_payment(df, idx)

            # find the extra amount available for the month
            extra = self.loan_budget_ - df.payment_temp.sum()
            # make extra payments
            extra = make_extra_payments(df, extra)

            # update total balance
            total_balance = df.balance.sum()

            # increment month
            m += 1

        # package results
        results = pd.Series({
            'indices'       : indices,
            'months'        : m,
            'total_payment' : df.principle.sum() + df.interest.sum() - extra
        })

        # save results from the scenario if no results are found, or if they are better results
        if not hasattr(self, 'results_'):
            self.results_ = results
        elif results.total_payment < self.results_.total_payment:
            self.results_ = results
