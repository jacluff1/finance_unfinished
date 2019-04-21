import numpy as np
import pandas as pd
import pdb
import AccountData as ad

data = ad.load_data()
whole = ad.select_whole_periods(data)

def annual_gross_jacob(hourly,**kwargs):
    show = kwargs['show'] if 'show' in kwargs else True
    gross = hourly * 40 * 52
    if show: print(f"gross: {gross}")
    return gross

def annual_taxes_jacob(gross,**kwargs):
    show = kwargs['show'] if 'show' in kwargs else True

    fb = pd.DataFrame()
    fb['rate'] = [.1, .12, .22, .24, .32, .35, .37]
    fb['floor'] = [0, 19400, 78950, 168400, 321450, 408200, 612350]

    ga = pd.DataFrame()
    ga['rate'] = [.01, .02, .03, .04, .05, .0575]
    ga['floor'] = [0, 1000, 3000, 5000, 7000, 10000]

    def get_taxes(brackets):
        taxes = 0
        for n in range(brackets.shape[0]-1):
            if gross < brackets.iloc[n].floor:
                continue
            elif gross < brackets.iloc[n+1].floor:
                taxable = gross - brackets.iloc[n].floor
                taxes += taxable * brackets.iloc[n].rate
            else:
                taxable = brackets.iloc[n+1].floor - brackets.iloc[n].floor
                taxes += taxable*brackets.iloc[n].rate
        if gross > brackets.iloc[brackets.shape[0]-1].floor:
            taxable = gross - brackets.iloc[brackets.shape[0]-1].floor
            taxes += taxable * brackets.iloc[brackets.shape[0]-1].rate
        return taxes

    fed_taxes = get_taxes(fb)
    state_taxes = get_taxes(ga)

    if show: print(f"federal taxes: {fed_taxes}\nstate taxes: {state_taxes}")
    return fed_taxes + state_taxes

def annual_net_jacob(hourly,**kwargs):
    show = kwargs['show'] if 'show' in kwargs else True
    if show: print("annual:")
    show = kwargs['show'] if 'show' in kwargs else True
    gross = annual_gross_jacob(hourly,**kwargs)
    taxes = annual_taxes_jacob(gross,**kwargs)
    health = 378*26
    if show: print(f"health: {health}\n")
    return gross - taxes - health

def monthly_expenses_jacob(hourly,**kwargs):
    show = kwargs['show'] if 'show' in kwargs else True
    visit_freq = kwargs['visit_freq'] if 'visit_freq' in kwargs else 1e10

    ex = {
        'rent'              : 1000,
        'wifi'              : 50,
        'utilities'         : 120,
        'transportation'    : 50 * 52/12,
        'saving'            : annual_net_jacob(hourly,**kwargs)*.05/12,
        'food'              : 300,
        'student_loans'     : annual_gross_jacob(hourly,show=False) * .1/12,
        'family_vist'       : 350 * 52/(12*visit_freq)
        }

    if show: print("monthly:")
    total = 0
    for key,expense in ex.items():
        total += expense
        if show: print(f"{key}: {round(expense,2)}")
    print(f"\ntotal monthly expenses: {round(total,2)}")

    return round(total,2)

def monthly_profit_jacob(hourly,**kwargs):
    show = kwargs['show'] if 'show' in kwargs else True
    net = annual_net_jacob(hourly,show=False)/12
    exp = monthly_expenses_jacob(hourly,**kwargs)
    if show: print(f"monthly net income: {round(net,2)}")
    profit = net - exp
    if show: print(f"monthly profit: {round(profit,2)}")
    return profit

#===============================================================================
#
#===============================================================================

def monthly_expenses_live_with_family(hourly,**kwargs):
    show = kwargs['show'] if 'show' in kwargs else True
    visit_freq = kwargs['visit_freq'] if 'visit_freq' in kwargs else 1e10

    ex = {
        'transportation'    : 50 * 52/12,
        'saving'            : annual_net_jacob(hourly,**kwargs)*.05/12,
        'food'              : 300,
        'student_loans'     : annual_gross_jacob(hourly,show=False) * .1/12,
        }

    if show: print("monthly:")
    total = 0
    for key,expense in ex.items():
        total += expense
        if show: print(f"{key}: {round(expense,2)}")
    print(f"\ntotal monthly expenses: {round(total,2)}")

    return round(total,2)

def monthly_profit_live_with_family(hourly,**kwargs):
    show = kwargs['show'] if 'show' in kwargs else True
    net = annual_net_jacob(hourly,show=False)/12
    exp = monthly_expenses_live_with_family(hourly,**kwargs)
    if show: print(f"monthly net income: {round(net,2)}")
    profit = net - exp
    if show: print(f"monthly profit: {round(profit,2)}")
    return profit
