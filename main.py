# import libraries
import expenses
import income
import dataCollection as dc
import loan

class main:

    def __init__(self):
        # construct and collect dataCollection instances
        instances           =   dict(massage_envy=dc.MASSAGE_ENVY(), calendar=dc.GOOGLE_CALENDAR(), bank=dc.DESERT_FINANTIAL(), jacob_stuLoans=dc.NAVIENT("navi-jacob"), amber_stuLoans=dc.NAVIENT("navi-amber"), credit_card=dc.DF_CARDMEMBER(), mortgage=dc.CARRINGTON())
        self.instances      =   pd.Series(instances)
        # collect DataFrames of instance data
        data                =   {}
        for inst in instances: data[key] = instances[key].GET_DATA()
        self.data           =   data
        # construct and collect loan instances
        loans               =   {}
        loan_list           =   ['bank', 'jacob_stuLoans', 'amber_stuLoans', 'credit_card', 'mortgage']
        for loan in loan_list:
            meta                =   instances[loan].GET_LOAN_META()
            loan_inst           =   loan.LOAN(meta)
            name                =   loan_inst.loan
            loans[name]         =   loan_inst
        self.loans          =   pd.Series(loans)

    def __GET_PLANNED_INCOME(self):
        NotImplemented

    def __GET_PLANNED_EXPENSES(self):
        NotImplemented

    def __GET_SAVINGS_PLAN(self):
        NotImplemented

    def __GET_DEBT_PLAN(self):
        NotImplemented

    def __GET_INVESTMENTS_PLAN(self):
        NotImplemented
