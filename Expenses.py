# import external dependencies
import pandas as pd
import pdb

# import internal dependencies
from Base import Base

#===============================================================================
# functions
#===============================================================================

#===============================================================================
# class definition
#===============================================================================

class Expenses(Base):

    def __init__(self, Loans, **kwargs):
        print("\nconstructing Expenses instance...")
        self.name_ = 'Expenses'
        super().__init__(**kwargs)

        self.__fill_in_planning_amounts(Loans)
        self.save_csv( 'plan_' )

        self.expenses_ = self.bills_.append(
            [ self.__format_loans(Loans), self.__format_plan() ],
            ignore_index = True,
            sort = False
            )
        self.save_csv( 'expenses_' )
        print(self.expenses_)
        total_expenses = self.expenses_.amount.sum()
        print(f"\ntotal expenses: \t {total_expenses:0.2f}")

        print("\nincome:\n")
        for key in self.income_:
            print(f"{key.replace('_', ' ')} \t {self.income_[key].item()/12:0.2f}")

        print(f"\nleft over: \t {self.income_.net.item()/12 - total_expenses:0.2f}")

    def __fill_in_planning_amounts(self, Loans):

        idx_map = self.get_index_map( ['emergency', 'fun', '401k'] )

        # zero out elements
        for idx in idx_map.values():
            self.plan_.loc[idx,'amount'] = 0

        # fill in the 401k amount
        idx = idx_map['401k']
        gross = self.income_.gross.item() / 12
        fraction = self.plan_.loc[idx,'fraction_of_gross']
        self.plan_.loc[idx,'amount'] = gross * fraction

        # fill in the emergency amount
        net = self.income_.net.item() / 12
        spending =\
            self.bills_.amount.sum() +\
            self.plan_.amount.sum() +\
            sum(Loans.payments_.values())
        left_over = net - spending
        for key in ['emergency', 'fun']:
            idx = idx_map[key]
            fraction = self.plan_.loc[idx,'fraction_remaining']
            self.plan_.loc[idx,'amount'] = left_over * fraction

        # round
        self.plan_.amount = self.plan_.amount.round(2)
        self.bills_.amount = self.bills_.amount.round(2)

    def __format_plan(self):
        return self.plan_[['name', 'amount', 'category']]

    def __format_loans(self, Loans):
        loans = Loans.payments_
        return pd.DataFrame({
            'name'      : [key for key in loans],
            'amount'    : [value for value in loans.values()],
            'category'  : 'loan'
        })
