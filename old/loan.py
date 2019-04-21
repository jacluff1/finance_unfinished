# import libraries
import math

class LOAN:

    def __init__(self,meta):
        # assign all the entries in meta dictionary to instance attributes
        for key in meta: setattr(self,key,meta[key])
        # assign Monthly Percentage and Daily Percentage Rates
        self.MPR                    =   self.APR/12
        self.DPR                    =   self.APR/365.25
        # create an empty data frame to track month, balance, principalPayment, interestPayment, payment
        columns                     =   ['month', 'balance', 'principalPayment', 'interestPayment', 'extraPayment', 'minimumPayment', 'payment']
        self.data                   =   pd.DataFrame(columns=columns)
        # add the first row into the data
        row                         =   {}
        row['month']                =   0
        row['balance']              =   meta['balance']
        row['interestPayment']      =   meta['balance'] * self.MPR
        row['minimumPayment']       =   self._GET_MINIMUM_PAYMENT()
        row['principalPayment']     =   row['minimumPayment'] - row['interestPayment']
        row['extraPayment']         =   0
        row['payment']              =   row['minimumPayment']
        row                         =   pd.Series(row)
        self.data                   =   self.data.append(row, ignore_index=True)

    #===============================================================================================
    # protected methods
    #===============================================================================================

    def _GET_MINIMUM_PAYMENT(self):
        if self.loan == "DF_Cardmember":
            return self.__DF_CARDMEMBER_MINIMUM_PAYMENT()
        elif hasattr(self,"minPayment"):
            return self.minPayment
        else:
            return self.__CALCULATE_MINIMUM_PAYMENT()

    def _ADD_DATA_ROW(self):
        # get latest row
        row0                        =   self.data.iloc[self.data.shape[0]]
        # create a dictionary to collect new row
        row                         =   {}
        row['month']                =   row0.month += 1
        row['interestPayment']      =   row0.balance * self.MPR
        row['minimumPayment']       =   self._GET_MINIMUM_PAYMENT()


        row['month']                =
        row['balance']              =   meta['balance']
        row['interestPayment']      =   meta['balance'] * self.MPR
        row['minimumPayment']       =   self._GET_MINIMUM_PAYMENT()
        row['principalPayment']     =   row['minimumPayment'] - row['interestPayment']
        row['extraPayment']         =   0
        row['payment']              =   row['minimumPayment']
        row                         =   pd.Series(row)
        self.data                   =   self.data.append(row, ignore_index=True)

    def _MAKE_MINIMUM_PAYMENT(self):
        NotImplemented

    def _MAKE_EXTRA_PAYMENT(self):
        NotImplemented

    def _PAYOFF_FROM_MIMINUM_PAYMENT(self):
        NotImplemented

    def _PAYOFF_FROM_EXTRA_PAYMENT(self):
        NotImplemented

    #===============================================================================================
    # private methods
    #===============================================================================================

    def __DF_CARDMEMBER_MINIMUM_PAYMENT(self):
        needs_attr      =   ['balance', 'MPR']
        for attr in needs_attr:
            assert hasattr(self,attr), "loan instance needs attribute - '%s' to calculate minimum payment." % attr
        base_payment    =   max(30, self.balance*.01)
        interest_charge =   self.balance * self.MPR
        return math.ceil(base_payment + interest_charge)

    def __CALCULATE_MINIMUM_PAYMENT(self):
        needs_attr      =   ['originalBalance', 'MPR', 'nPer']
        for attr in needs_attr:
            assert hasattr(self,attr), "loan instance needs attribute - '%s' to calculate minimum payment." % attr
        A   =   self.originalBalance
        B   =   (1 + self.MPR)**self.nPer
        D   =   (B - 1) / (self.MPR * B)
        return A / D

    def __GET_INTEREST_PAYMENT(self):
        NotImplemented

    def __GET_PRINCIPAL_PAYMENT(self):
        NotImplemented
