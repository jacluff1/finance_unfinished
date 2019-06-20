# import external dependencies
import pandas as pd

# import internal dependencies
from Base import Base

#===============================================================================
# functions
#===============================================================================

def annual_taxes(gross, brackets):

    taxes = 0
    for i in range(brackets.shape[0]-1):
        if gross < brackets.iloc[i].floor:
            continue
        elif gross < brackets.iloc[i+1].floor:
            taxable = gross - brackets.iloc[i].floor
            taxes += taxable * brackets.iloc[i].rate
        else:
            taxable = brackets.iloc[i+1].floor - brackets.iloc[i].floor
            taxes += taxable*brackets.iloc[i].rate
    if gross > brackets.iloc[brackets.shape[0]-1].floor:
        taxable = gross - brackets.iloc[brackets.shape[0]-1].floor
        taxes += taxable * brackets.iloc[brackets.shape[0]-1].rate
    return taxes

#===============================================================================
# kwargs
#===============================================================================

kwargs = {
    'csv_'      : {
        'income_'           : 'Income.csv',
        'federal_bracket_'  : 'Federal_brackets_2019.csv',
        'state_bracket_'    : 'AZ_brackets_2019.csv'
    },
    'gross_'    : 69e3,
}

#===============================================================================
# class definition
#===============================================================================

class Income(Base):

    def __init__(self, **kwargs):
        print("\nconstructing Income instance...")
        super().__init__(**kwargs)

        # calculate incomes
        federal_taxes = annual_taxes( self.gross_, self.federal_bracket_ )
        state_taxes = annual_taxes( self.gross_, self.state_bracket_ )
        net = self.gross_ - federal_taxes - state_taxes

        # collect and calculate income
        self.income_ = pd.DataFrame({
            'gross'         : self.gross_,
            'federal_taxes' : federal_taxes,
            'state_taxes'   : state_taxes,
            'net'           : net
        }, index=[0])

        # round to 2 decimal places
        self.income_ = self.income_.round(2)

        # print income
        print("\nincome:")
        for key in self.income_:
            name = key.replace('_', ' ')
            print(f"{name}: {self.income_[key].item()}")

        self.save_csv( 'income_' )

#===============================================================================
# main
#===============================================================================

if __name__ == '__main__':
    income = Income(**kwargs)
